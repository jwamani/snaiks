# basic_behavior.py: Basic behavior system for snakes with performance optimizations
import random
import math
from functools import lru_cache
from pygame.math import Vector2
from settings import *

class BasicBehavior:
    """Handles AI decision making for snakes"""
    
    @staticmethod
    def calculate_direction(snake, food_items, other_snakes):
        """Calculate optimal direction for a snake based on current game state"""
        if snake.is_dead:
            return Vector2(0, 0)
        
        # Find nearest food
        nearest_food = BasicBehavior.find_nearest_food(snake, food_items)
        
        # Find threats (larger snakes if current snake is a hunter target)
        threats = BasicBehavior.find_threats(snake, other_snakes)
        
        # Find prey (smaller snakes if current snake is a hunter)
        prey = BasicBehavior.find_prey(snake, other_snakes)
        
        # Calculate desired direction based on priorities
        direction = BasicBehavior.calculate_behavior_vector(snake, nearest_food, threats, prey)
        
        return direction
    
    @staticmethod
    def find_nearest_food(snake, food_items):
        """Find the nearest food item to the snake - optimized using min() with key function"""
        if not food_items:
            return None
        
        # One-line optimization using min() with key function
        return min(food_items, key=lambda food: BasicBehavior._cached_distance(
            snake.head_position.x, snake.head_position.y, 
            food.position.x, food.position.y), default=None)
    
    @staticmethod
    def find_threats(snake, other_snakes):
        """Find threatening snakes (hunters larger than current snake) - optimized with list comprehension"""
        return [
            other_snake for other_snake in other_snakes
            if (other_snake != snake and 
                not other_snake.is_dead and
                other_snake.is_hunter and 
                other_snake.size > snake.size + FEAR_MARGIN and
                BasicBehavior._cached_distance(
                    snake.head_position.x, snake.head_position.y,
                    other_snake.head_position.x, other_snake.head_position.y) < THREAT_AVOIDANCE_DISTANCE)
        ]
    
    @staticmethod
    def find_prey(snake, other_snakes):
        """Find potential prey (smaller snakes if current snake is hunter) - optimized with list comprehension"""
        if not snake.is_hunter:
            return []
        
        return [
            other_snake for other_snake in other_snakes
            if (other_snake != snake and 
                not other_snake.is_dead and
                other_snake.size < snake.size - FEAR_MARGIN and
                BasicBehavior._cached_distance(
                    snake.head_position.x, snake.head_position.y,
                    other_snake.head_position.x, other_snake.head_position.y) < THREAT_AVOIDANCE_DISTANCE)
        ]
    
    @staticmethod
    def calculate_behavior_vector(snake, nearest_food, threats, prey):
        """Calculate the final movement vector based on all factors"""
        final_direction = Vector2(0, 0)
        
        # 1. Handle threats (high priority)
        if threats:
            threat_avoidance = BasicBehavior.calculate_threat_avoidance(snake, threats)
            final_direction += threat_avoidance * 2.5  # Slightly reduced weight
            
            # Allow hunters to still consider prey even when threats exist
            if prey and snake.is_hunter:
                # Only pursue if the hunter is significantly bigger than prey
                closest_prey = min(prey, key=lambda p: BasicBehavior._cached_distance(
                    snake.head_position.x, snake.head_position.y,
                    p.head_position.x, p.head_position.y))
                size_advantage = snake.size - closest_prey.size
                
                if size_advantage > FEAR_MARGIN * 1.5:
                    prey_pursuit = BasicBehavior.calculate_prey_pursuit(snake, prey)
                    # Weight depends on size advantage
                    pursuit_weight = 1.5 + (size_advantage / 10)
                    final_direction += prey_pursuit * pursuit_weight
        
        # 2. Hunt prey (medium-high priority for hunters)
        elif prey and snake.is_hunter:
            prey_pursuit = BasicBehavior.calculate_prey_pursuit(snake, prey)
            final_direction += prey_pursuit * 2.5  # Increased weight for more aggressive hunting
        
        # 3. Seek food (medium priority)
        elif nearest_food:
            food_seeking = BasicBehavior.calculate_food_seeking(snake, nearest_food)
            final_direction += food_seeking * 1.5  # Medium weight
        
        # 4. Avoid walls (always active)
        wall_avoidance = BasicBehavior.calculate_wall_avoidance(snake)
        final_direction += wall_avoidance * 1.0  # Base weight
        
        # 5. Random exploration if no other stimulus
        if final_direction.length_squared() < 0.1:
            final_direction = BasicBehavior.calculate_random_movement(snake)
        
        # Normalize and return
        if final_direction.length_squared() > 0:
            final_direction.normalize_ip()
            
        return final_direction
    
    @staticmethod
    def calculate_threat_avoidance(snake, threats):
        """Calculate direction to avoid threats"""
        avoidance_vector = Vector2(0, 0)
        
        for threat in threats:
            # Vector from threat to snake (direction to flee)
            flee_direction = snake.head_position - threat.head_position
            if flee_direction.length_squared() > 0:
                # Closer threats have more influence
                distance = flee_direction.length()
                flee_direction.normalize_ip()
                # Inverse relationship: closer = stronger avoidance
                strength = THREAT_AVOIDANCE_DISTANCE / max(distance, 1)
                avoidance_vector += flee_direction * strength
                
        return avoidance_vector
    
    @staticmethod
    def calculate_prey_pursuit(snake, prey):
        """Calculate direction to pursue prey"""
        if not prey:
            return Vector2(0, 0)
            
        # Target the closest prey
        closest_prey = min(prey, key=lambda p: BasicBehavior._cached_distance(
            snake.head_position.x, snake.head_position.y,
            p.head_position.x, p.head_position.y))
        
        # Vector from snake to prey
        pursuit_direction = closest_prey.head_position - snake.head_position
        
        if pursuit_direction.length_squared() > 0:
            pursuit_direction.normalize_ip()
            
        return pursuit_direction
    
    @staticmethod
    def calculate_food_seeking(snake, food):
        """Calculate direction to seek food"""
        if not food:
            return Vector2(0, 0)
            
        # Vector from snake to food
        food_direction = food.position - snake.head_position
        
        if food_direction.length_squared() > 0:
            food_direction.normalize_ip()
            
        return food_direction
    
    @staticmethod
    def calculate_wall_avoidance(snake):
        """Calculate direction to avoid walls"""
        avoidance = Vector2(0, 0)
        pos = snake.head_position
        
        # Check distance to each wall
        dist_to_left = pos.x
        dist_to_right = SCREEN_WIDTH - pos.x
        dist_to_top = pos.y
        dist_to_bottom = SCREEN_HEIGHT - pos.y
        
        # Apply avoidance force if too close to walls
        if dist_to_left < WALL_AVOIDANCE_DISTANCE:
            avoidance.x += (WALL_AVOIDANCE_DISTANCE - dist_to_left) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_right < WALL_AVOIDANCE_DISTANCE:
            avoidance.x -= (WALL_AVOIDANCE_DISTANCE - dist_to_right) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_top < WALL_AVOIDANCE_DISTANCE:
            avoidance.y += (WALL_AVOIDANCE_DISTANCE - dist_to_top) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_bottom < WALL_AVOIDANCE_DISTANCE:
            avoidance.y -= (WALL_AVOIDANCE_DISTANCE - dist_to_bottom) / WALL_AVOIDANCE_DISTANCE
            
        return avoidance * PROACTIVE_AVOIDANCE_STRENGTH
    
    @staticmethod
    def calculate_random_movement(snake):
        """Calculate random movement direction"""
        # Use snake's current velocity as a basis for momentum
        if snake.velocity.length_squared() > 0:
            # Add some randomness to current direction
            current_dir = snake.velocity.normalize()
            random_offset = Vector2(
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3)
            )
            return current_dir + random_offset
        else:
            # Completely random direction
            return Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
    
    @staticmethod
    @lru_cache(maxsize=1024)
    def _cached_distance(x1, y1, x2, y2):
        """Cached distance calculation for performance optimization"""
        dx = x2 - x1
        dy = y2 - y1
        return (dx*dx + dy*dy) ** 0.5
