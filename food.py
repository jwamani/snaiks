# food.py: Defines the Food class and special food types
import pygame
import random
import time
import math
from settings import *
from pygame.math import Vector2


class Food:
    def __init__(self, food_type="normal"):
        self.position = Vector2(
            random.randint(FOOD_RADIUS, SCREEN_WIDTH - FOOD_RADIUS),
            random.randint(FOOD_RADIUS, SCREEN_HEIGHT - FOOD_RADIUS),
        )
        self.radius = FOOD_RADIUS
        self.food_type = food_type
        self.creation_time = time.time()

        # Set properties based on food type
        self._setup_food_properties()

    def _setup_food_properties(self):
        """Setup visual and effect properties based on food type"""
        if self.food_type == "normal":
            self.color = FOOD_COLOR
            self.effect_description = "Basic nutrition"

        elif self.food_type == "speed":
            self.color = SPEED_FOOD_COLOR
            self.effect_description = (
                f"Speed boost x{SPEED_FOOD_BOOST_MULTIPLIER} for {SPEED_FOOD_DURATION}s"
            )

        elif self.food_type == "slow":
            self.color = SLOW_FOOD_COLOR
            self.effect_description = f"Speed reduction x{SLOW_FOOD_REDUCTION_MULTIPLIER} for {SLOW_FOOD_DURATION}s"

        elif self.food_type == "immunity":
            self.color = IMMUNITY_FOOD_COLOR
            self.effect_description = (
                f"Immunity from hunters for {IMMUNITY_FOOD_DURATION}s"
            )

        elif self.food_type == "growth":
            self.color = GROWTH_FOOD_COLOR
            self.effect_description = (
                f"Instant growth +{GROWTH_FOOD_SIZE_BONUS} segments"
            )        
        elif self.food_type == "shrink":
            self.color = SHRINK_FOOD_COLOR
            self.effect_description = (
                f"Size reduction -{SHRINK_FOOD_SIZE_REDUCTION} segments"
            )

        elif self.food_type == "energy":
            self.color = ENERGY_FOOD_COLOR
            self.effect_description = f"Energy boost +{ENERGY_FOOD_RESTORATION} energy"

        elif self.food_type == "health":
            self.color = HEALTH_FOOD_COLOR
            self.effect_description = f"Instant healing +{HEALTH_FOOD_RESTORATION} HP"

        else:
            # Fallback to normal food
            self.color = FOOD_COLOR
            self.effect_description = "Basic nutrition"

    def draw(self, screen):
        """Draw the food with special effects for different types"""
        age = time.time() - self.creation_time

        if self.food_type == "normal":
            # Simple circle for normal food
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.position.x), int(self.position.y)),
                self.radius,
            )

        elif self.food_type == "speed":
            # Pulsing cyan food with speed lines
            pulse = 0.8 + 0.2 * math.sin(age * 8)
            radius = int(self.radius * pulse)
            pygame.draw.circle(
                screen, self.color, (int(self.position.x), int(self.position.y)), radius
            )

            # Speed lines around the food
            for i in range(4):
                angle = age * 10 + i * 90
                line_length = self.radius + 5
                end_x = self.position.x + line_length * math.cos(math.radians(angle))
                end_y = self.position.y + line_length * math.sin(math.radians(angle))
                pygame.draw.line(
                    screen,
                    self.color,
                    (int(self.position.x), int(self.position.y)),
                    (int(end_x), int(end_y)),
                    2,
                )

        elif self.food_type == "slow":
            # Purple food with concentric circles
            for i in range(3):
                alpha = int(100 - i * 30)
                radius = self.radius + i * 3
                slow_color = (*self.color, alpha)
                slow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(slow_surface, slow_color, (radius, radius), radius)
                screen.blit(
                    slow_surface, (self.position.x - radius, self.position.y - radius)
                )

        elif self.food_type == "immunity":
            # Gold food with shimmering effect
            shimmer = int(200 + 55 * math.sin(age * 6))
            shimmer_color = (shimmer, shimmer - 50, 0)
            pygame.draw.circle(
                screen,
                shimmer_color,
                (int(self.position.x), int(self.position.y)),
                self.radius,
            )

            # Golden aura
            aura_radius = self.radius + 3
            aura_alpha = int(80 + 40 * math.sin(age * 4))
            aura_color = (255, 215, 0, aura_alpha)
            aura_surface = pygame.Surface(
                (aura_radius * 2, aura_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                aura_surface, aura_color, (aura_radius, aura_radius), aura_radius
            )
            screen.blit(
                aura_surface,
                (self.position.x - aura_radius, self.position.y - aura_radius),
            )

        elif self.food_type == "growth":
            # Orange food with expanding rings
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.position.x), int(self.position.y)),
                self.radius,
            )

            # Expanding rings
            for i in range(2):
                ring_phase = (age * 3 + i * 1.5) % 3
                ring_radius = self.radius + ring_phase * 8
                ring_alpha = int(100 * (1 - ring_phase / 3))
                if ring_alpha > 0:
                    ring_color = (*self.color, ring_alpha)
                    ring_surface = pygame.Surface(
                        (ring_radius * 2, ring_radius * 2), pygame.SRCALPHA
                    )
                    pygame.draw.circle(
                        ring_surface,
                        ring_color,
                        (int(ring_radius), int(ring_radius)),
                        int(ring_radius),
                        2,
                    )
                    screen.blit(
                        ring_surface,
                        (self.position.x - ring_radius, self.position.y - ring_radius),
                    )        
        elif self.food_type == "shrink":
            # Pink food with contracting effect
            contraction = 0.9 + 0.1 * math.sin(age * 10)
            radius = int(self.radius * contraction)
            pygame.draw.circle(
                screen, self.color, (int(self.position.x), int(self.position.y)), radius
            )

        elif self.food_type == "energy":
            # Energy food with electric sparks effect
            pulse = 0.8 + 0.4 * math.sin(age * 10)
            radius = int(self.radius * pulse)

            # Draw main energy food circle
            pygame.draw.circle(
                screen, self.color, (int(self.position.x), int(self.position.y)), radius
            )

            # Draw lightning bolt symbol
            bolt_size = radius // 2
            bolt_points = [
                (self.position.x - bolt_size//2, self.position.y - bolt_size),
                (self.position.x + bolt_size//4, self.position.y - bolt_size//4),
                (self.position.x - bolt_size//4, self.position.y),
                (self.position.x + bolt_size//2, self.position.y + bolt_size),
                (self.position.x - bolt_size//4, self.position.y + bolt_size//4),
                (self.position.x + bolt_size//4, self.position.y)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), bolt_points)

            # Energy sparks
            for i in range(3):
                spark_angle = age * 5 + i * 120
                spark_radius = radius + 8 + 3 * math.sin(age * 8 + i)
                spark_x = self.position.x + spark_radius * math.cos(math.radians(spark_angle))
                spark_y = self.position.y + spark_radius * math.sin(math.radians(spark_angle))
                pygame.draw.circle(screen, (255, 255, 255), (int(spark_x), int(spark_y)), 2)

        elif self.food_type == "health":
            # Health food with pulsing heart effect
            pulse = 0.8 + 0.3 * math.sin(age * 6)
            radius = int(self.radius * pulse)

            # Draw main health food circle
            pygame.draw.circle(
                screen, self.color, (int(self.position.x), int(self.position.y)), radius
            )

            # Draw healing cross symbol
            cross_size = radius // 2
            cross_width = 2
            # Horizontal line
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    int(self.position.x - cross_size),
                    int(self.position.y - cross_width // 2),
                    cross_size * 2,
                    cross_width,
                ),
            )
            # Vertical line
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    int(self.position.x - cross_width // 2),
                    int(self.position.y - cross_size),
                    cross_width,
                    cross_size * 2,
                ),
            )

            # Healing aura
            aura_radius = radius + 5
            aura_alpha = int(60 + 30 * math.sin(age * 4))
            aura_color = (255, 200, 200, aura_alpha)
            aura_surface = pygame.Surface(
                (aura_radius * 2, aura_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                aura_surface, aura_color, (aura_radius, aura_radius), aura_radius, 3
            )
            screen.blit(
                aura_surface,
                (self.position.x - aura_radius, self.position.y - aura_radius),
            )

    def draw_arcade(self, arcade_window):
        """Draw food using Arcade graphics with enhanced visual effects"""
        import arcade
        import math

        age = time.time() - self.creation_time

        if self.food_type == "normal":
            # Basic food with simple glow
            arcade.draw_circle_filled(
                self.position.x, self.position.y, self.radius, self.color
            )
            # Subtle glow
            arcade.draw_circle_outline(
                self.position.x, self.position.y, self.radius + 2, (*self.color, 100), 2
            )

        elif self.food_type == "speed":
            # Speed food with electric effects
            pulse = 0.8 + 0.4 * math.sin(age * 8)
            radius = int(self.radius * pulse)

            # Main circle
            arcade.draw_circle_filled(
                self.position.x, self.position.y, radius, self.color
            )

            # Electric bolts effect
            for i in range(4):
                angle = age * 10 + i * 90
                line_length = self.radius + 5
                end_x = self.position.x + line_length * math.cos(math.radians(angle))
                end_y = self.position.y + line_length * math.sin(math.radians(angle))
                arcade.draw_line(
                    self.position.x, self.position.y, end_x, end_y, self.color, 2
                )

        elif self.food_type == "slow":
            # Purple food with concentric circles
            arcade.draw_circle_filled(
                self.position.x, self.position.y, self.radius, self.color
            )
            for i in range(3):
                radius = self.radius + i * 3
                alpha = max(50, 100 - i * 30)
                slow_color = (*self.color, alpha)
                arcade.draw_circle_outline(
                    self.position.x, self.position.y, radius, slow_color, 2
                )

        elif self.food_type == "immunity":
            # Gold food with shimmering effect
            shimmer = int(200 + 55 * math.sin(age * 6))
            shimmer_color = (shimmer, max(0, shimmer - 50), 0)
            arcade.draw_circle_filled(
                self.position.x, self.position.y, self.radius, shimmer_color
            )

            # Golden aura
            aura_radius = self.radius + 3
            aura_alpha = int(80 + 40 * math.sin(age * 4))
            aura_color = (255, 215, 0, aura_alpha)
            arcade.draw_circle_outline(
                self.position.x, self.position.y, aura_radius, aura_color, 3
            )

        elif self.food_type == "growth":
            # Orange food with expanding rings
            arcade.draw_circle_filled(
                self.position.x, self.position.y, self.radius, self.color
            )

            # Expanding rings
            for ring in range(3):
                ring_phase = (age * 2 + ring) % 3
                ring_radius = self.radius + ring_phase * 10
                ring_alpha = max(20, int(100 * (1 - ring_phase / 3)))
                ring_color = (*self.color, ring_alpha)
                arcade.draw_circle_outline(
                    self.position.x, self.position.y, ring_radius, ring_color, 2
                )        
        elif self.food_type == "shrink":
            # Pink food with contracting effect
            contraction = 0.9 + 0.1 * math.sin(age * 10)
            radius = int(self.radius * contraction)
            arcade.draw_circle_filled(
                self.position.x, self.position.y, radius, self.color
            )

        elif self.food_type == "energy":
            # Energy food with electric sparks effect
            pulse = 0.8 + 0.4 * math.sin(age * 10)
            radius = int(self.radius * pulse)

            # Main energy food circle
            arcade.draw_circle_filled(
                self.position.x, self.position.y, radius, self.color
            )

            # Lightning bolt effect (simplified for arcade)
            for i in range(4):
                angle = age * 12 + i * 90
                line_length = radius + 8
                end_x = self.position.x + line_length * math.cos(math.radians(angle))
                end_y = self.position.y + line_length * math.sin(math.radians(angle))
                arcade.draw_line(
                    self.position.x, self.position.y, end_x, end_y, arcade.color.WHITE, 3
                )

            # Energy sparks
            for i in range(3):
                spark_angle = age * 8 + i * 120
                spark_radius = radius + 10 + 3 * math.sin(age * 6 + i)
                spark_x = self.position.x + spark_radius * math.cos(math.radians(spark_angle))
                spark_y = self.position.y + spark_radius * math.sin(math.radians(spark_angle))
                arcade.draw_circle_filled(spark_x, spark_y, 3, arcade.color.WHITE)

        elif self.food_type == "health":
            # Health food with pulsing heart effect
            pulse = 0.8 + 0.3 * math.sin(age * 6)
            radius = int(self.radius * pulse)

            # Draw main health food circle
            arcade.draw_circle_filled(
                self.position.x, self.position.y, radius, self.color
            )  # Draw healing cross symbol
            cross_size = radius // 2
            cross_width = 2  # Horizontal line of cross
            arcade.draw_lrbt_rectangle_filled(
                self.position.x - cross_size,
                self.position.x + cross_size,
                self.position.y - cross_width // 2,
                self.position.y + cross_width // 2,
                arcade.color.WHITE,
            )
            # Vertical line of cross
            arcade.draw_lrbt_rectangle_filled(
                self.position.x - cross_width // 2,
                self.position.x + cross_width // 2,
                self.position.y - cross_size,
                self.position.y + cross_size,
                arcade.color.WHITE,
            )

            # Healing aura
            aura_radius = radius + 5
            aura_alpha = int(60 + 30 * math.sin(age * 4))
            aura_color = (255, 200, 200, aura_alpha)
            arcade.draw_circle_outline(
                self.position.x, self.position.y, aura_radius, aura_color, 3
            )

        else:
            # Fallback to basic circle
            arcade.draw_circle_filled(
                self.position.x, self.position.y, self.radius, self.color
            )


def create_food(force_type=None):
    """Factory function to create food with appropriate type"""
    if not ENABLE_SPECIAL_FOOD or force_type == "normal":
        return Food("normal")

    if force_type:
        return Food(force_type)

    # Random chance for special food
    if random.random() < SPECIAL_FOOD_SPAWN_CHANCE:
        # Choose random special food type from enabled types
        available_types = []

        if ENABLE_SPEED_FOOD:
            available_types.append("speed")
        if ENABLE_SLOW_FOOD:
            available_types.append("slow")
        if ENABLE_IMMUNITY_FOOD:
            available_types.append("immunity")
        if ENABLE_GROWTH_FOOD:
            available_types.append("growth")        
        if ENABLE_SHRINK_FOOD:
            available_types.append("shrink")
        if ENABLE_ENERGY_FOOD:
            available_types.append("energy")
        if ENABLE_HEALTH_FOOD:
            available_types.append("health")

        # Always enable health food for testing the health system if not already added
        if "health" not in available_types:
            available_types.append("health")

        if available_types:
            food_type = random.choice(available_types)
            return Food(food_type)

    # Default to normal food
    return Food("normal")
