# environmental_effect.py: Base class for environmental effects
import pygame
import random
from pygame.math import Vector2
from settings import *
import time
import uuid
import random


class EnvironmentalEffect:
    """Base class for all environmental effects"""

    def __init__(self, x, y, lifetime=10.0):
        self.id = str(uuid.uuid4())[:8]  # Unique ID for each effect
        self.position = Vector2(x, y)
        self.creation_time = time.time()
        self.lifetime = lifetime
        self.is_active = True
        self.effect_type = "base"

    def update(self, snakes, food_items, creatures):
        """Update effect - override in subclasses"""
        # Check if effect should expire
        if time.time() - self.creation_time > self.lifetime:
            self.is_active = False

    def apply_effect(self, entities):
        """Apply effect to entities - override in subclasses"""
        pass

    def draw(self, screen):
        """Draw effect - override in subclasses"""
        pass

    def is_expired(self):
        """Check if effect has expired"""
        return not self.is_active or (time.time() - self.creation_time > self.lifetime)


class BlackHoleEffect(EnvironmentalEffect):
    """Black hole that pulls entities toward its center"""

    def __init__(self, x, y):
        super().__init__(x, y, BLACK_HOLE_LIFETIME)
        self.effect_type = "black_hole"
        self.radius = BLACK_HOLE_RADIUS
        self.pull_radius = BLACK_HOLE_PULL_RADIUS
        self.pull_strength = BLACK_HOLE_PULL_STRENGTH

        # Visual effects
        self.rotation = 0.0
        self.pulse_phase = 0.0

    def update(self, snakes, food_items, creatures):
        """Update black hole and apply gravitational effects"""
        super().update(snakes, food_items, creatures)

        if not self.is_active:
            return

        # Update visual effects
        self.rotation += 5.0  # Rotation speed
        self.pulse_phase += 0.2

        # Apply gravitational pull to snakes
        for snake in snakes:
            if snake.is_dead:
                continue
            self._apply_gravitational_pull(snake)

        # Apply gravitational pull to food items
        for food in food_items:
            self._apply_gravitational_pull_to_food(food)

        # Apply gravitational pull to creatures
        all_creatures = []
        if hasattr(creatures, "get_all_creatures"):
            all_creatures = creatures.get_all_creatures()
        elif hasattr(creatures, "rippers"):
            all_creatures.extend(creatures.rippers)
        elif hasattr(creatures, "scavengers"):
            all_creatures.extend(creatures.scavengers)

        for creature in all_creatures:
            if hasattr(creature, "is_dead") and creature.is_dead:
                continue
            self._apply_gravitational_pull(creature)

    def _apply_gravitational_pull(self, entity):
        """Apply gravitational pull to an entity (snake or creature)"""
        # Calculate distance to black hole
        distance_vector = (
            self.position - entity.head_position
            if hasattr(entity, "head_position")
            else self.position - entity.position
        )
        distance = distance_vector.length()

        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 5:  # Avoid division by zero
            # Calculate pull force (stronger when closer)
            pull_force = (
                self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            )

            # Normalize direction vector
            pull_direction = distance_vector.normalize()

            # Apply pull to entity's velocity
            if hasattr(entity, "velocity"):
                entity.velocity += pull_direction * pull_force * 0.3  # Dampen effect

    def _apply_gravitational_pull_to_food(self, food):
        """Apply gravitational pull to food items"""
        distance_vector = self.position - food.position
        distance = distance_vector.length()

        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 5:
            # Calculate pull force
            pull_force = (
                self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            )

            # Normalize direction vector
            pull_direction = distance_vector.normalize()

            # Move food toward black hole
            food.position += pull_direction * pull_force * 0.1

    def draw(self, screen):
        """Draw the black hole with visual effects"""
        if not self.is_active:
            return

        import math

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)  # Fade out over time

        # Draw gravitational field (faint outer ring)
        field_alpha = int(30 * age_factor)
        field_color = (50, 0, 50, field_alpha)
        field_surface = pygame.Surface(
            (self.pull_radius * 2, self.pull_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            field_surface,
            field_color,
            (self.pull_radius, self.pull_radius),
            self.pull_radius,
            2,
        )
        screen.blit(
            field_surface,
            (self.position.x - self.pull_radius, self.position.y - self.pull_radius),
        )

        # Draw main black hole body
        main_radius = int(self.radius * age_factor)
        if main_radius > 0:
            # Pulsing dark center
            pulse = int(50 + 30 * math.sin(self.pulse_phase))
            center_color = (pulse, 0, pulse)
            pygame.draw.circle(
                screen,
                center_color,
                (int(self.position.x), int(self.position.y)),
                main_radius,
            )

            # Darker inner circle
            inner_radius = int(main_radius * 0.7)
            pygame.draw.circle(
                screen,
                (20, 0, 20),
                (int(self.position.x), int(self.position.y)),
                inner_radius,
            )

            # Rotating accretion disk effect
            for i in range(8):
                angle = self.rotation + i * 45
                ring_radius = main_radius + 10 + i * 3
                ring_x = self.position.x + ring_radius * math.cos(math.radians(angle))
                ring_y = self.position.y + ring_radius * math.sin(math.radians(angle))

                ring_alpha = int(100 * age_factor * (8 - i) / 8)
                ring_color = (ring_alpha, 0, ring_alpha // 2)

                if ring_alpha > 0:
                    pygame.draw.circle(
                        screen, ring_color, (int(ring_x), int(ring_y)), 3
                    )

    def draw_arcade(self, arcade_window):
        """Draw black hole using Arcade graphics with enhanced visual effects"""
        import arcade
        import math

        if not self.is_active:
            return

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Draw gravitational field (outer ring)
        field_radius = int(self.pull_radius * age_factor)
        if field_radius > 0:
            arcade.draw_circle_outline(
                self.position.x, self.position.y, field_radius, (50, 0, 50, 80), 3
            )

        # Draw main black hole body with pulsing effect
        main_radius = int(self.radius * age_factor)
        if main_radius > 0:
            # Pulsing dark center
            pulse = 0.5 + 0.3 * math.sin(self.pulse_phase)
            center_alpha = int(200 * pulse * age_factor)

            arcade.draw_circle_filled(
                self.position.x,
                self.position.y,
                main_radius,
                (int(50 * pulse), 0, int(50 * pulse), center_alpha),
            )

            # Darker inner circle
            inner_radius = int(main_radius * 0.7)
            arcade.draw_circle_filled(
                self.position.x,
                self.position.y,
                inner_radius,
                (20, 0, 20, center_alpha + 50),
            )

            # Rotating accretion disk effect
            for i in range(8):
                angle = self.rotation + i * 45
                ring_radius = main_radius + 10 + i * 3
                ring_x = self.position.x + ring_radius * math.cos(math.radians(angle))
                ring_y = self.position.y + ring_radius * math.sin(math.radians(angle))

                ring_alpha = int(150 * age_factor * (8 - i) / 8)
                if ring_alpha > 0:
                    arcade.draw_circle_filled(
                        ring_x, ring_y, 3, (ring_alpha, 0, ring_alpha // 2, ring_alpha)
                    )


class SpeedZoneEffect(EnvironmentalEffect):
    """Zone that modifies movement speed of entities within it"""

    def __init__(self, x, y, is_fast_zone=True):
        super().__init__(x, y, SPEED_ZONE_LIFETIME)
        self.effect_type = "speed_zone"
        self.radius = SPEED_ZONE_RADIUS
        self.is_fast_zone = is_fast_zone
        self.speed_multiplier = (
            SPEED_ZONE_FAST_MULTIPLIER if is_fast_zone else SPEED_ZONE_SLOW_MULTIPLIER
        )

        # Visual effects
        self.pulse_phase = 0.0

    def update(self, snakes, food_items, creatures):
        """Update speed zone effects"""
        super().update(snakes, food_items, creatures)

        if not self.is_active:
            return

        self.pulse_phase += 0.1

        # Apply speed effects to snakes
        for snake in snakes:
            if snake.is_dead:
                continue
            self._apply_speed_effect(snake)

        # Apply speed effects to creatures
        all_creatures = []
        if hasattr(creatures, "get_all_creatures"):
            all_creatures = creatures.get_all_creatures()

        for creature in all_creatures:
            if hasattr(creature, "is_dead") and creature.is_dead:
                continue
            self._apply_speed_effect(creature)

    def _apply_speed_effect(self, entity):
        """Apply speed modification to entity if within zone"""
        entity_pos = (
            entity.head_position
            if hasattr(entity, "head_position")
            else entity.position
        )
        distance = (self.position - entity_pos).length()

        if distance < self.radius:
            # Temporarily modify entity's max speed
            if hasattr(entity, "max_speed"):
                # Store original speed if not already stored
                if not hasattr(entity, "_original_max_speed"):
                    entity._original_max_speed = entity.max_speed

                entity.max_speed = entity._original_max_speed * self.speed_multiplier
        else:
            # Restore original speed when outside zone
            if hasattr(entity, "_original_max_speed"):
                entity.max_speed = entity._original_max_speed
                delattr(entity, "_original_max_speed")

    def draw(self, screen):
        """Draw the speed zone with visual effects"""
        if not self.is_active:
            return

        import math

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.5 + 0.3 * math.sin(self.pulse_phase)

        # Different colors for fast vs slow zones
        if self.is_fast_zone:
            base_color = (0, 255, 100)  # Green for speed boost
        else:
            base_color = (255, 100, 0)  # Orange for speed reduction

        # Draw zone boundary
        alpha = int(80 * age_factor * pulse)
        zone_color = (*base_color, alpha)
        zone_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            zone_surface, zone_color, (self.radius, self.radius), self.radius, 3
        )
        screen.blit(
            zone_surface, (self.position.x - self.radius, self.position.y - self.radius)
        )

        # Draw center indicator
        center_radius = int(8 * pulse)
        pygame.draw.circle(
            screen,
            base_color,
            (int(self.position.x), int(self.position.y)),
            center_radius,
        )

    def draw_arcade(self, arcade_window):
        """Draw speed zone using Arcade graphics with enhanced visual effects"""
        import arcade
        import math

        if not self.is_active:
            return

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.5 + 0.3 * math.sin(self.pulse_phase)

        # Different colors for fast vs slow zones
        if self.is_fast_zone:
            base_color = (0, 255, 100)  # Green for speed boost
        else:
            base_color = (255, 100, 0)  # Orange for speed reduction

        # Draw zone boundary
        alpha = int(80 * age_factor * pulse)
        zone_color = (*base_color, alpha)
        arcade.draw_circle_outline(
            self.position.x, self.position.y, self.radius, zone_color, 3
        )

        # Draw center indicator
        center_radius = int(8 * pulse)
        arcade.draw_circle_filled(
            self.position.x, self.position.y, center_radius, base_color
        )

        # Draw speed lines for fast zones
        if self.is_fast_zone:
            for i in range(8):
                angle = (self.pulse_phase * 2 + i * 45) % 360
                line_start_x = self.position.x + (center_radius + 5) * math.cos(
                    math.radians(angle)
                )
                line_start_y = self.position.y + (center_radius + 5) * math.sin(
                    math.radians(angle)
                )
                line_end_x = self.position.x + (center_radius + 15) * math.cos(
                    math.radians(angle)
                )
                line_end_y = self.position.y + (center_radius + 15) * math.sin(
                    math.radians(angle)
                )
                arcade.draw_line(
                    line_start_x, line_start_y, line_end_x, line_end_y, base_color, 2
                )


class FoodMagnetEffect(EnvironmentalEffect):
    """Effect that attracts food items to a central point"""

    def __init__(self, x, y):
        super().__init__(x, y, FOOD_MAGNET_LIFETIME)
        self.effect_type = "food_magnet"
        self.radius = FOOD_MAGNET_RADIUS
        self.pull_radius = FOOD_MAGNET_PULL_RADIUS
        self.pull_strength = FOOD_MAGNET_PULL_STRENGTH

        # Visual effects
        self.pulse_phase = 0.0

    def update(self, snakes, food_items, creatures):
        """Update food magnet and attract food"""
        super().update(snakes, food_items, creatures)

        if not self.is_active:
            return

        self.pulse_phase += 0.15

        # Apply attraction to food items
        for food in food_items:
            self._attract_food(food)

    def _attract_food(self, food):
        """Attract food item toward magnet center"""
        distance_vector = self.position - food.position
        distance = distance_vector.length()

        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 10:  # Keep some minimum distance
            # Calculate attraction force
            attraction_force = (
                self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            )

            # Normalize direction vector
            pull_direction = distance_vector.normalize()

            # Move food toward magnet
            food.position += pull_direction * attraction_force * 0.2

    def draw(self, screen):
        """Draw the food magnet with visual effects"""
        if not self.is_active:
            return

        import math

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.6 + 0.4 * math.sin(self.pulse_phase)

        # Draw attraction field
        field_alpha = int(40 * age_factor * pulse)
        field_color = (255, 200, 0, field_alpha)
        field_surface = pygame.Surface(
            (self.pull_radius * 2, self.pull_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            field_surface,
            field_color,
            (self.pull_radius, self.pull_radius),
            self.pull_radius,
            2,
        )
        screen.blit(
            field_surface,
            (self.position.x - self.pull_radius, self.position.y - self.pull_radius),
        )

        # Draw magnet core
        core_radius = int(self.radius * age_factor * pulse)
        if core_radius > 0:
            pygame.draw.circle(
                screen,
                (255, 200, 0),
                (int(self.position.x), int(self.position.y)),
                core_radius,
            )

            # Inner sparkle effect
            inner_radius = int(core_radius * 0.5)
            pygame.draw.circle(
                screen,
                (255, 255, 150),
                (int(self.position.x), int(self.position.y)),
                inner_radius,
            )

    def draw_arcade(self, arcade_window):
        """Draw food magnet using Arcade graphics with enhanced visual effects"""
        import arcade
        import math

        if not self.is_active:
            return

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.6 + 0.4 * math.sin(self.pulse_phase)

        # Draw attraction field
        field_alpha = int(40 * age_factor * pulse)
        field_color = (255, 200, 0, field_alpha)
        arcade.draw_circle_outline(
            self.position.x, self.position.y, self.pull_radius, field_color, 2
        )

        # Draw magnet core
        core_radius = int(self.radius * age_factor * pulse)
        if core_radius > 0:
            arcade.draw_circle_filled(
                self.position.x, self.position.y, core_radius, (255, 200, 0)
            )

            # Inner sparkle effect
            inner_radius = int(core_radius * 0.5)
            arcade.draw_circle_filled(
                self.position.x, self.position.y, inner_radius, (255, 255, 150)
            )

        # Draw magnetic field lines
        for i in range(8):
            angle = (self.pulse_phase + i * 45) % 360
            inner_x = self.position.x + core_radius * math.cos(math.radians(angle))
            inner_y = self.position.y + core_radius * math.sin(math.radians(angle))
            outer_x = self.position.x + (self.pull_radius * 0.8) * math.cos(
                math.radians(angle)
            )
            outer_y = self.position.y + (self.pull_radius * 0.8) * math.sin(
                math.radians(angle)
            )

            line_alpha = int(60 * age_factor * pulse)
            line_color = (255, 200, 0, line_alpha)
            arcade.draw_line(inner_x, inner_y, outer_x, outer_y, line_color, 1)


class PoisonZoneEffect(EnvironmentalEffect):
    """Poison zone that damages entities and drifts with wind patterns"""

    def __init__(self, x, y):
        super().__init__(x, y, POISON_ZONE_LIFETIME)
        self.effect_type = "poison_zone"
        self.radius = POISON_ZONE_RADIUS
        self.damage_rate = POISON_ZONE_DAMAGE_RATE
        self.lingering_duration = POISON_ZONE_LINGERING_DURATION

        # Wind movement system
        self.wind_direction = (
            Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            if random.random() > 0
            else Vector2(1, 0)
        )
        self.wind_speed = POISON_ZONE_WIND_SPEED

        # Visual effects
        self.pulse_phase = 0.0
        self.swirl_rotation = 0.0

        # Damage tracking for entities
        self.entities_inside = set()  # Track which entities are currently inside
        self.lingering_poison = {}  # Track entities with lingering poison effects

    def update(self, snakes, food_items, creatures):
        """Update poison zone, handle movement, and apply damage"""
        super().update(snakes, food_items, creatures)

        if not self.is_active:
            return

        # Update visual effects
        self.pulse_phase += POISON_ZONE_PULSE_SPEED
        self.swirl_rotation += 2.0  # Rotation speed for swirling effect

        # Drift with wind patterns
        wind_movement = (
            self.wind_direction * self.wind_speed * (1 / 60)
        )  # Assume 60 FPS
        self.position += wind_movement

        # Handle screen wrapping for poison zones
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

        # Collect all entities to check
        all_entities = []
        for snake in snakes:
            if not snake.is_dead:
                all_entities.append(snake)

        # Add creatures if available
        if hasattr(creatures, "get_all_creatures"):
            all_entities.extend(creatures.get_all_creatures())
        elif hasattr(creatures, "rippers"):
            all_entities.extend(creatures.rippers)
        elif hasattr(creatures, "scavengers"):
            all_entities.extend(creatures.scavengers)

        # Track which entities are currently inside
        currently_inside = set()

        for entity in all_entities:
            if hasattr(entity, "is_dead") and entity.is_dead:
                continue

            entity_pos = (
                entity.head_position
                if hasattr(entity, "head_position")
                else entity.position
            )
            distance = (self.position - entity_pos).length()

            if distance < self.radius:
                currently_inside.add(entity.id if hasattr(entity, "id") else id(entity))
                self._apply_poison_damage(entity)
            else:
                # Check if entity just left the zone
                entity_id = entity.id if hasattr(entity, "id") else id(entity)
                if entity_id in self.entities_inside:
                    self._start_lingering_poison(entity)

        # Update entities_inside set
        self.entities_inside = currently_inside

        # Update lingering poison effects
        self._update_lingering_poison(all_entities)

    def _apply_poison_damage(self, entity):
        """Apply poison damage to entity inside the zone"""
        if hasattr(entity, "apply_environmental_damage"):
            # Apply damage at the specified rate (assuming 60 FPS)
            damage_per_frame = self.damage_rate / 30.0
            entity.apply_environmental_damage("poison", damage_per_frame)

    def _start_lingering_poison(self, entity):
        """Start lingering poison effect when entity leaves the zone"""
        entity_id = entity.id if hasattr(entity, "id") else id(entity)
        self.lingering_poison[entity_id] = {
            "entity": entity,
            "start_time": time.time(),
            "duration": self.lingering_duration,
        }

    def _update_lingering_poison(self, all_entities):
        """Update lingering poison effects on entities that left the zone"""
        current_time = time.time()
        expired_entities = []

        for entity_id, poison_data in self.lingering_poison.items():
            entity = poison_data["entity"]
            elapsed_time = current_time - poison_data["start_time"]

            if elapsed_time >= poison_data["duration"]:
                expired_entities.append(entity_id)
            elif hasattr(entity, "apply_environmental_damage") and not (
                hasattr(entity, "is_dead") and entity.is_dead
            ):
                # Apply reduced lingering damage
                lingering_damage_per_frame = (
                    self.damage_rate * 0.5
                ) / 45.0  # Half damage while lingering
                entity.apply_environmental_damage("poison", lingering_damage_per_frame)

        # Remove expired lingering effects
        for entity_id in expired_entities:
            del self.lingering_poison[entity_id]

    def draw(self, screen):
        """Draw the poison zone with swirling toxic visual effects"""
        if not self.is_active:
            return

        import math
        import random

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.7 + 0.3 * math.sin(self.pulse_phase)

        # Base colors for poison zone (purple-green toxic)
        base_color = (
            100 + int(50 * pulse),
            200 + int(55 * pulse),
            100 + int(30 * pulse),
        )
        warning_color = (150, 255, 150)

        # Draw warning border (larger radius)
        warning_radius = int(self.radius + 15)
        warning_alpha = int(60 * age_factor * pulse)
        warning_surface = pygame.Surface(
            (warning_radius * 2, warning_radius * 2), pygame.SRCALPHA
        )
        warning_zone_color = (*warning_color, warning_alpha)
        pygame.draw.circle(
            warning_surface,
            warning_zone_color,
            (warning_radius, warning_radius),
            warning_radius,
            4,
        )
        screen.blit(
            warning_surface,
            (self.position.x - warning_radius, self.position.y - warning_radius),
        )

        # Draw main poison zone with swirling effect
        zone_alpha = int(120 * age_factor * pulse)
        zone_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )

        # Create swirling pattern
        for ring in range(3):
            ring_radius = int(self.radius * (0.3 + ring * 0.3))
            ring_alpha = zone_alpha // (ring + 1)
            ring_color = (*base_color, ring_alpha)

            # Rotate each ring at different speeds
            rotation_offset = self.swirl_rotation * (ring + 1) * 0.5

            # Draw swirl segments
            for segment in range(8):
                angle = (segment * 45 + rotation_offset) % 360
                start_angle = math.radians(angle)
                end_angle = math.radians(angle + 30)

                # Calculate arc points (simplified as polygon)
                points = []
                center = (self.radius, self.radius)
                for i in range(5):
                    interpolated_angle = start_angle + (end_angle - start_angle) * (
                        i / 4
                    )
                    x = center[0] + ring_radius * math.cos(interpolated_angle)
                    y = center[1] + ring_radius * math.sin(interpolated_angle)
                    points.append((x, y))

                if len(points) >= 3:
                    pygame.draw.polygon(zone_surface, ring_color, points)

        screen.blit(
            zone_surface, (self.position.x - self.radius, self.position.y - self.radius)
        )

        # Draw toxic particles around the zone
        for i in range(6):
            particle_angle = (time.time() * 50 + i * 60) % 360
            particle_distance = self.radius + 10 + 15 * math.sin(time.time() * 3 + i)
            particle_x = self.position.x + particle_distance * math.cos(
                math.radians(particle_angle)
            )
            particle_y = self.position.y + particle_distance * math.sin(
                math.radians(particle_angle)
            )

            particle_alpha = int(100 * age_factor * pulse)
            particle_color = (80, 255, 120, particle_alpha)
            particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, (3, 3), 3)
            screen.blit(particle_surface, (particle_x - 3, particle_y - 3))    
    def draw_arcade(self, arcade_window):
        """Draw poison zone using Arcade graphics with enhanced visual effects"""
        import arcade
        import math

        if not self.is_active:
            return

        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)

        # Pulsing effect
        pulse = 0.7 + 0.3 * math.sin(self.pulse_phase)

        # Base colors for poison zone (purple-green toxic)
        base_color = (
            100 + int(50 * pulse),
            200 + int(55 * pulse),
            100 + int(30 * pulse),
        )
        warning_color = (150, 255, 150)

        # Draw warning border (larger radius)
        warning_radius = int(self.radius + 15)
        warning_alpha = int(60 * age_factor * pulse)
        if warning_radius > 0:
            arcade.draw_circle_outline(
                self.position.x,
                self.position.y,
                warning_radius,
                (*warning_color, warning_alpha),
                3,
            )

        # Draw main poison zone with simple filled circle
        zone_alpha = int(120 * age_factor * pulse)
        zone_color = (*base_color, zone_alpha)
        arcade.draw_circle_filled(
            self.position.x, self.position.y, self.radius, zone_color
        )

        # Draw swirling rings
        for ring in range(3):
            ring_radius = int(self.radius * (0.3 + ring * 0.3))
            ring_alpha = max(20, zone_alpha // (ring + 1))
            ring_color = (*base_color, ring_alpha)

            # Rotate each ring at different speeds
            rotation_offset = self.swirl_rotation * (ring + 1) * 0.5

            arcade.draw_circle_outline(
                self.position.x, self.position.y, ring_radius, ring_color, 2
            )

        # Draw toxic particles around the zone
        for i in range(6):
            particle_angle = (time.time() * 50 + i * 60) % 360
            particle_distance = self.radius + 10 + 15 * math.sin(time.time() * 3 + i)
            particle_x = self.position.x + particle_distance * math.cos(
                math.radians(particle_angle)
            )
            particle_y = self.position.y + particle_distance * math.sin(
                math.radians(particle_angle)
            )

            particle_alpha = int(100 * age_factor * pulse)
            particle_color = (80, 255, 120, particle_alpha)
            arcade.draw_circle_filled(particle_x, particle_y, 3, particle_color)
