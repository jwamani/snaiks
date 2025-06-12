# game_manager.py: Handles game logic, spawning, collisions, state
import pygame
import random
import time
from settings import *
from snake import Snake
from food import create_food
from food_effects import FoodEffectsManager
from pygame.math import Vector2
from basic_behavior import BasicBehavior
from resource_manager import ResourceManager
from creature_manager import CreatureManager
from effects_manager import EffectsManager
from sound_manager import SoundManager

class GameManager:
    def __init__(self):
        self.snakes = []
        self.food_items = []
        self.score = 0
        self.game_over = False
        self.winner = None
        self.last_food_spawn_time = time.time()
        self.last_snake_spawn_time = time.time()
        # Resource management
        self.resource_manager = ResourceManager()
        
        # Sound effects management
        self.sound_manager = SoundManager()
        
        # Enhanced UI management
        from ui_enhancements import UIManager
        self.ui_manager = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Creature management - modular system
        self.creature_manager = CreatureManager(self.sound_manager)
        
        # Environmental effects management
        self.effects_manager = EffectsManager(self.sound_manager)
        
        # Food effects management for special food
        self.food_effects_manager = FoodEffectsManager()
        
        # Performance tracking
        self.frame_count = 0
        self.last_performance_update = time.time()
        
        # Spawn initial food items
        self.spawn_initial_food()

    def update(self):
        """Update game state, including snakes and food."""
        self.resource_manager.start_frame()
        # Update snakes with AI behavior
        for snake in self.snakes[:]:  # Use slice copy to allow safe removal
            if snake.is_dead:
                continue
                
            # Check starvation status for each snake with sound effects
            snake.check_starvation(self.sound_manager)
            
            # Skip further processing if snake died from starvation
            if snake.is_dead:
                continue
                
            # Calculate basic behavior direction for snake
            ai_direction = BasicBehavior.calculate_direction(snake, self.food_items, self.snakes)
            
            # Move snake with AI direction
            snake.move(ai_direction)
        
        # Update spatial grid for efficient collision detection
        self.resource_manager.update_spatial_grid(self.snakes, self.food_items)
        
        # Check for collisions and update game state
        self.check_collisions()
        
        # Clean up dead snakes periodically
        if self.resource_manager.should_cleanup():
            self.cleanup_dead_snakes()

        # Spawn food if needed - spawn multiple at once to reach target
        if len(self.food_items) < MAX_FOOD_ON_SCREEN:
            if time.time() - self.last_food_spawn_time > FOOD_SPAWN_INTERVAL:
                # Spawn multiple food items to quickly reach the target
                food_to_spawn = min(5, MAX_FOOD_ON_SCREEN - len(self.food_items))
                for _ in range(food_to_spawn):
                    self.spawn_food()
                self.last_food_spawn_time = time.time()

        # Spawn new snakes if needed
        if len(self.snakes) < MAX_SNAKES_ON_SCREEN and time.time() - self.last_snake_spawn_time > random.uniform(SNAKE_SPAWN_INTERVAL_MIN, SNAKE_SPAWN_INTERVAL_MAX):
            self.spawn_snake()
            self.last_snake_spawn_time = time.time()
        
        # Update creatures using the modular creature manager
        self.creature_manager.update(self.snakes, self.food_items)
          # Update food effects on snakes
        self.food_effects_manager.update_effects(self.snakes)
          # Update health regeneration for all snakes
        for snake in self.snakes:
            if not snake.is_dead:
                # TODO: Check if snake is in safe zone or territory when those systems are implemented
                snake.update_health_regeneration(in_safe_zone=False, in_territory=False)
                snake.update_poison_effects()  # Update poison visual effects
                
                # TEMPORARY: Test damage system - ENABLED for health bar testing
                # Comment out the next 5 lines to disable test damage for normal gameplay
                # if random.random() < 0.002:  # 0.2% chance per frame (~1 damage every 8-10 seconds)
                #     damage_types = ["poison", "disaster", "aerial_attack"]
                #     damage_type = random.choice(damage_types)
                #     snake.apply_environmental_damage(damage_type, 1, self.sound_manager)
                #     print(f"Snake {snake.id[:4]} took {damage_type} damage! HP: {snake.hp}/{snake.max_hp}")
        
        # Update environmental effects
        self.effects_manager.update(self.snakes, self.food_items, self.creature_manager)
        
        self.resource_manager.mark_update_complete()
        
        # Print performance stats occasionally
        self.frame_count += 1
        if self.frame_count % 300 == 0:  # Every 5 seconds at 60 FPS
            self.print_performance_stats()

    def check_collisions(self):
        """Check for collisions between snakes and food, and snake-to-snake collisions."""
        # Food collisions
        for snake in self.snakes:
            if snake.is_dead:
                continue
                
            for food in self.food_items[:]:  # Use slice copy for safe removal
                if snake.head_position.distance_to(food.position) < (SNAKE_SEGMENT_RADIUS + food.radius):
                    # Apply food effects based on food type
                    self.food_effects_manager.apply_food_effect(snake, food.food_type)
                    
                    # Normal growth (special foods may have additional effects)
                    snake.grow()
                    
                    self.food_items.remove(food)
                    self.resource_manager.return_food_to_pool(food)
        
        # Snake-to-snake collisions (hunter eating smaller snakes)
        for hunter in self.snakes:
            if not hunter.is_hunter or hunter.is_dead:
                continue
                
            for prey in self.snakes:
                if prey == hunter or prey.is_dead:
                    continue
                
                # Check if prey has immunity effect active
                prey_effects = self.food_effects_manager.get_snake_effects(prey.id)
                is_immune = any(effect.effect_type == "immunity" for effect in prey_effects)
                
                if is_immune:
                    continue  # Skip immune snakes
                
                # Hunter can eat smaller snakes
                if (prey.size < hunter.size - FEAR_MARGIN and
                    hunter.head_position.distance_to(prey.head_position) < SNAKE_SEGMENT_RADIUS * 2):
                    break  # Hunter can only eat one snake per frame
    
    def spawn_food(self):
        """Spawn a new food item using the special food creation system."""
        food = create_food()  # Use the special food factory function
        self.food_items.append(food)
        
        # Play food spawn sound effect
        # self.sound_manager.play_food_spawn_sound()
    
    def spawn_initial_food(self):
        """Spawn initial food items to populate the screen"""
        for _ in range(MAX_FOOD_ON_SCREEN):
            self.spawn_food()

    def spawn_snake(self):
        """Spawn a new snake at a random position with random color."""
        # Generate random position
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)

        # Generate random color variation for visual diversity
        color_variation = (
            random.randint(-20, 20),
            random.randint(-20, 20),
            random.randint(-20, 20)
        )

        # Create base color - either use normal snake color or a random variation
        if random.random() < 0.8:  # 80% chance of normal color
            base_color = NORMAL_SNAKE_BODY_COLOR
        else:
            # Generate a completely random color
            base_color = (
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 200)
            )

        # Apply variation to the base color
        color = (
            max(0, min(255, base_color[0] + color_variation[0])),
            max(0, min(255, base_color[1] + color_variation[1])),
            max(0, min(255, base_color[2] + color_variation[2]))
        )        # Create and add the snake
        new_snake = Snake(x, y, color)
          # TEMPORARY: Give new snakes some damage so we can see health bars immediately
        new_snake.take_damage(2, "spawn_test")  # Take only 2 damage so HP = 8/10
        print(f"New snake spawned with {new_snake.hp}/{new_snake.max_hp} HP for health bar testing")

        # Give random initial direction
        direction = Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
        if direction.length_squared() > 0:
            direction.normalize_ip()
            new_snake.move(direction)

        self.snakes.append(new_snake)
        
        # Play snake spawn sound effect
        # self.sound_manager.play_snake_spawn_sound()
    
    def cleanup_dead_snakes(self):
        """Remove dead snakes that have been dead for a while"""
        current_time = time.time()
        
        # Remove snakes that have been dead for more than 3 seconds
        self.snakes = [snake for snake in self.snakes 
                      if not snake.is_dead or (current_time - getattr(snake, 'death_time', current_time)) < 3.0]
    
    def print_performance_stats(self):
        """Print performance statistics to console"""
        stats = self.resource_manager.get_performance_stats()
        creature_counts = self.creature_manager.get_creature_counts()
        effect_counts = self.effects_manager.get_effect_counts()        
        print(f"FPS: {stats.get('fps', 0):.1f}, "
              f"Snakes: {len([s for s in self.snakes if not s.is_dead])}, "
              f"Food: {len(self.food_items)}, "
              f"Rippers: {creature_counts.get('rippers', 0)}, "
              f"Scavengers: {creature_counts.get('scavengers', 0)}, "
              f"BlackHoles: {effect_counts.get('black_holes', 0)}, "
              f"SpeedZones: {effect_counts.get('speed_zones', 0)}, "
              f"FoodMagnets: {effect_counts.get('food_magnets', 0)}, "
              f"PoisonZones: {effect_counts.get('poison_zones', 0)}, "
              f"Update: {stats.get('update_time_ms', 0):.1f}ms")

    def draw(self, screen):
        """Draw all game elements on the screen."""
        # Draw food items
        for food in self.food_items:
            food.draw(screen)

        # Draw snakes with their active effects
        for snake in self.snakes:
            # Get active effects for this snake to show visual indicators
            active_effects = self.food_effects_manager.get_snake_effects(snake.id)
            snake.draw(screen, active_effects)

        # Draw creatures using the modular creature manager
        self.creature_manager.draw(screen)
        
        # Draw environmental effects
        self.effects_manager.draw(screen)
          # Draw enhanced UI with survival statistics
        game_stats = self.ui_manager.get_game_stats(self.snakes, self.food_items, self.effects_manager)
        self.ui_manager.draw_enhanced_hud(screen, game_stats)
        
        # Draw enhanced snake info for critical snakes
        for snake in self.snakes:
            self.ui_manager.draw_enhanced_snake_info(screen, snake)
        
        self.resource_manager.mark_draw_complete()
