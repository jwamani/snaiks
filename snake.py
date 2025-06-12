# snake.py: Defines the Snake class
import pygame
import math
import time
import uuid # For unique snake IDs
from pygame.math import Vector2
from settings import *

class Snake:
    def __init__(self, initial_pos_x, initial_pos_y, color=None, initial_length=INITIAL_SNAKE_LENGTH):
        self.id = str(uuid.uuid4())[:8] # Unique ID for each snake

        self.body_segments = [] # List of Vector2 positions for each segment
        self.head_position = Vector2(initial_pos_x, initial_pos_y)

        self.is_hunter = False # Initialize first
        self.body_color = NORMAL_SNAKE_BODY_COLOR
        self.head_color = NORMAL_SNAKE_HEAD_COLOR
        if color: # Allow specific color override if provided, though hunter status will change it
            self.body_color = color
            self.head_color = (min(255,color[0]+20), min(255,color[1]+20), min(255,color[2]+20))

        self.initial_length = initial_length

        self.velocity = Vector2(0, 0) # Current velocity
        self.max_speed = BASE_MAX_SPEED
        self.acceleration_rate = BASE_ACCELERATION
        
        self.size = initial_length # Number of segments including head
        self.food_eaten = 0
        self.is_dead = False
        
        # Health System - Foundational survival mechanic
        self.max_hp = 10  # Maximum health points
        self.hp = self.max_hp  # Current health points
        self.last_damage_time = 0  # Track when last damage was taken
        self.damage_source = None  # Track source of last damage
        self.healing_rate = 0.2  # HP per second natural regeneration (increased for better balance)
        self.last_heal_time = time.time()  # Track healing timing
        
        # Starvation tracking
        self.last_food_time = time.time()  # Track when snake last ate food
        self.is_starving = False  # Visual indicator for starvation warning
        self.starvation_warning_played = False  # Track if warning sound was played
        self.starvation_critical_played = False  # Track if critical sound was played
        
        # Poison effects tracking
        self.is_poisoned = False  # Visual indicator for being in poison zone
        self.poison_intensity = 0.0  # Intensity of poison effect for visuals

        self.recent_growth_time = 0  # Track recent growth for visual effect
        self.recent_shrink_time = 0  # Track recent shrinking for visual effect

        self.last_decision_time = time.time()
        self.alive = True

        # Initialize body
        for i in range(self.initial_length):
            # Segments initially overlap by half their radius for a connected look
            self.body_segments.append(Vector2(self.head_position.x - i * SNAKE_SEGMENT_RADIUS * 1.0, self.head_position.y))
        if self.body_segments:
            self.head_position = self.body_segments[0]

        self.update_dynamic_properties()

    def update_dynamic_properties(self):
        """Updates speed and acceleration based on size."""
        # Inverse relationship: larger snake, slower and less agile
        self.max_speed = BASE_MAX_SPEED / (1 + (self.size - self.initial_length) * SIZE_SPEED_PENALTY_FACTOR)
        self.acceleration_rate = BASE_ACCELERATION / (1 + (self.size - self.initial_length) * SIZE_ACCEL_PENALTY_FACTOR)
        # Ensure they don't go to zero or negative
        self.max_speed = max(0.5, self.max_speed) # Minimum speed
        self.acceleration_rate = max(0.05, self.acceleration_rate) # Minimum acceleration

    def move(self, target_direction: Vector2 = None, nearest_food=None, nearest_hunter=None, min_food_dist=None, min_hunter_dist=None):
        if self.is_dead:
            return

        if target_direction and target_direction.length_squared() > 0:
            desired_velocity = target_direction.normalize() * self.max_speed
            steering = (desired_velocity - self.velocity)
            if steering.length_squared() > 0:
                steering = steering.normalize() * self.acceleration_rate
            self.velocity += steering

        # Cap speed
        if self.velocity.length_squared() > self.max_speed * self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Update head position
        new_head_position = self.head_position + self.velocity

        # Move body segments
        self.body_segments.insert(0, new_head_position)
        if len(self.body_segments) > self.size:
            self.body_segments.pop()

        self.head_position = self.body_segments[0]
        self.handle_screen_wrap()

    def grow(self, amount=1, reason="ate food"):
        if self.is_dead: return
        self.size += amount

        # Reset starvation timer when eating food
        if reason == "ate food":
            self.last_food_time = time.time()
            self.is_starving = False
            
        # Track recent growth for visual effects
        if amount > 1:  # Special food growth
            self.recent_growth_time = time.time()

        if not self.is_hunter:
            if reason == "ate food":
                self.food_eaten += amount
            if self.food_eaten >= FOOD_TO_BECOME_HUNTER:
                self.is_hunter = True
                self.body_color = HUNTER_SNAKE_BODY_COLOR
                self.head_color = HUNTER_SNAKE_HEAD_COLOR
        self.update_dynamic_properties()

    def handle_screen_wrap(self):
        if self.is_dead: return

        if WALL_BEHAVIOR == "wraparound":
            wrapped = False
            if self.head_position.x > SCREEN_WIDTH + SNAKE_SEGMENT_RADIUS: # Allow going slightly off before wrap
                self.head_position.x = -SNAKE_SEGMENT_RADIUS
                wrapped = True
            elif self.head_position.x < -SNAKE_SEGMENT_RADIUS:
                self.head_position.x = SCREEN_WIDTH + SNAKE_SEGMENT_RADIUS
                wrapped = True
            if self.head_position.y > SCREEN_HEIGHT + SNAKE_SEGMENT_RADIUS:
                self.head_position.y = -SNAKE_SEGMENT_RADIUS
                wrapped = True
            elif self.head_position.y < -SNAKE_SEGMENT_RADIUS:
                self.head_position.y = SCREEN_HEIGHT + SNAKE_SEGMENT_RADIUS
                wrapped = True

            if wrapped:
                self.body_segments[0] = self.head_position

        elif WALL_BEHAVIOR == "destructive":
            # Check if center of head is out of bounds
            if not (0 <= self.head_position.x <= SCREEN_WIDTH and \
                    0 <= self.head_position.y <= SCREEN_HEIGHT):
                self.die(reason="hit wall")

    def check_self_collision(self):
        # Self-collision is disabled for now; always return False
        return False

    def check_starvation(self, sound_manager=None):
        """Check if snake is starving and handle starvation death"""
        if self.is_dead or not ENABLE_STARVATION:
            return
        
        current_time = time.time()
        time_since_food = current_time - self.last_food_time
        
        # Check if snake should die from starvation
        if time_since_food >= STARVATION_TIME:
            # Play critical starvation sound before death
            if sound_manager and not self.starvation_critical_played:
                sound_manager.play_starvation_critical_sound()
                self.starvation_critical_played = True
            self.die(reason="starvation")
            return
        
        # Check if snake is entering starvation warning state
        if time_since_food >= STARVATION_WARNING_TIME:
            self.is_starving = True
            # Play warning sound when first entering starvation warning
            if sound_manager and not self.starvation_warning_played:
                sound_manager.play_starvation_warning_sound()
                self.starvation_warning_played = True
        else:
            # Reset starvation state and sound flags when no longer starving
            self.is_starving = False
            self.starvation_warning_played = False
            self.starvation_critical_played = False

    def die(self, reason="unknown"):
        if not self.is_dead:
            self.is_dead = True
            self.hp = 0  # Set HP to 0 when dead
            self.death_time = time.time()  # Track when snake died
            self.body_color = DEAD_SNAKE_COLOR
            self.head_color = DEAD_SNAKE_COLOR

    def take_damage(self, amount, source="unknown", sound_manager=None):
        """Apply damage to the snake and handle death if HP reaches 0"""
        if self.is_dead:
            return False
        
        self.hp = max(0, self.hp - amount)
        self.last_damage_time = time.time()
        self.damage_source = source
        
        # Play appropriate damage sound
        if sound_manager and amount > 0:
            if source == "poison":
                sound_manager.play_sound("poison_damage", volume=0.2)
            elif source == "disaster":
                sound_manager.play_sound("disaster_damage", volume=0.3)
            elif source == "aerial_attack":
                sound_manager.play_sound("aerial_damage", volume=0.4)
            elif source == "combat":
                sound_manager.play_sound("combat_damage", volume=0.3)
        
        # Check if snake dies from damage
        if self.hp <= 0:
            self.die(reason=f"killed by {source}")
            return True  # Snake died
        
        return False  # Snake survived
    
    def heal(self, amount, source="natural"):
        """Heal the snake by specified amount, up to max HP"""
        if self.is_dead:
            return 0
        
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        actual_healing = self.hp - old_hp
        
        if actual_healing > 0:
            self.last_heal_time = time.time()
            
        return actual_healing
    
    def update_health_regeneration(self, in_safe_zone=False, in_territory=False):
        """Handle natural health regeneration based on environment"""
        if self.is_dead or self.hp >= self.max_hp:
            return
        
        current_time = time.time()
        time_since_last_heal = current_time - self.last_heal_time
        
        # Calculate regeneration rate based on environment
        regen_rate = self.healing_rate
        if in_safe_zone:
            regen_rate *= 2  # Double healing in safe zones
        if in_territory:
            regen_rate *= 1.5  # Bonus healing in owned territory
        
        # Apply regeneration every second
        if time_since_last_heal >= 1.0:
            healing_amount = regen_rate * time_since_last_heal
            self.heal(healing_amount, source="regeneration")
    
    def update_poison_effects(self):
        """Update poison visual effects and decay over time"""
        if self.is_poisoned:
            # Decay poison intensity over time
            self.poison_intensity = max(0.0, self.poison_intensity - 0.02)  # Decay rate
            if self.poison_intensity <= 0.0:
                self.is_poisoned = False

    def get_health_percentage(self):
        """Get current health as a percentage of max health"""
        if self.max_hp <= 0:
            return 0
        return (self.hp / self.max_hp) * 100
    
    def is_critically_injured(self):
        """Check if snake is in critical health condition (< 30% HP)"""
        return self.get_health_percentage() < 30
    
    def is_heavily_injured(self):
        """Check if snake is heavily injured (< 50% HP)"""
        return self.get_health_percentage() < 50
    
    def get_health_status(self):
        """Get descriptive health status"""
        percentage = self.get_health_percentage()
        if percentage >= 80:
            return "healthy"
        elif percentage >= 50:
            return "lightly_injured"
        elif percentage >= 30:
            return "heavily_injured"
        else:
            return "critically_injured"
    def apply_environmental_damage(self, damage_type, damage_amount, sound_manager=None):
        """Apply damage from environmental sources"""
        if self.is_dead:
            return False
          # Different environmental damage types
        if damage_type == "poison":
            self.is_poisoned = True  # Set poison visual effect
            self.poison_intensity = min(1.0, self.poison_intensity + 0.1)  # Increase intensity
            return self.take_damage(damage_amount, "poison", sound_manager)  # Use actual damage amount
        elif damage_type == "acid_rain":
            return self.take_damage(2, "disaster", sound_manager)  # 2 HP per second in acid rain
        elif damage_type == "ice_storm":
            return self.take_damage(0.5, "disaster", sound_manager)  # Slower damage from ice
        elif damage_type == "heat_wave":
            return self.take_damage(0.5, "disaster", sound_manager)  # Heat damage
        elif damage_type == "aerial_attack":
            return self.take_damage(3, "aerial_attack", sound_manager)  # 3 HP from hawk attacks
        else:
            return self.take_damage(damage_amount, damage_type, sound_manager)
    
    def consume_health_food(self, sound_manager=None):
        """Special healing when consuming health food"""
        if self.is_dead:
            return 0
        
        healing_amount = 3  # Health food provides 3 HP instant restoration
        actual_healing = self.heal(healing_amount, source="health_food")
        
        if sound_manager and actual_healing > 0:
            sound_manager.play_sound("health_food_consumed", volume=0.3)
        
        return actual_healing

    def draw(self, screen, active_effects=None):
        if self.is_dead and len(self.body_segments) == 0: # Don't draw if truly gone
            return

        # Get active effects for visual indicators
        effects = active_effects or []
        
        # Draw body segments first
        for segment_pos in reversed(self.body_segments):
            # If dead, draw all segments in dead color
            if self.is_dead:
                color_to_use = DEAD_SNAKE_COLOR           
            elif self.is_starving:
                # Starving snakes get a pulsing orange/yellow color
                pulse = int(128 + 127 * math.sin(time.time() * 8))  # Fast pulsing
                if self.is_hunter:
                    color_to_use = (pulse, pulse//2, 0)  # Orange pulse for starving hunters
                else:
                    color_to_use = (pulse, pulse, 0)  # Yellow pulse for starving normal snakes
            else:
                # Check for active food effects and modify color accordingly
                color_to_use = self.body_color
                
                # Apply poison visual effect if poisoned
                if self.is_poisoned:
                    # Green toxic tint with pulsing effect
                    poison_pulse = int(100 + 100 * math.sin(time.time() * 6) * self.poison_intensity)
                    color_to_use = (
                        max(0, min(255, self.body_color[0] - 30)),
                        max(0, min(255, self.body_color[1] + poison_pulse)),
                        max(0, min(255, self.body_color[2] - 20))
                    )
                else:
                    # Check for active food effects
                    for effect in effects:
                        if effect.effect_type == "speed_boost":
                            # Cyan tint for speed boost
                            boost_pulse = int(50 + 50 * math.sin(time.time() * 12))
                            color_to_use = (
                                max(0, min(255, self.body_color[0] + boost_pulse)),
                                max(0, min(255, self.body_color[1] + boost_pulse)),
                                max(0, min(255, self.body_color[2] + 100 + boost_pulse))
                            )
                            break
                        elif effect.effect_type == "slow":
                            # Purple tint for slow effect
                            color_to_use = (
                                max(0, min(255, self.body_color[0] + 50)),
                                max(0, min(255, self.body_color[1] - 50)),
                                max(0, min(255, self.body_color[2] + 80))
                            )
                            break
                
            pygame.draw.circle(screen, color_to_use, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for detail
            inner_color_detail = (max(0,color_to_use[0]-30), max(0,color_to_use[1]-30), max(0,color_to_use[2]-30))
            pygame.draw.circle(screen, inner_color_detail, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

        # Draw head on top, potentially with a different color
        if self.body_segments: # Ensure there's a head to draw
            head_draw_pos = self.body_segments[0]
            
            if self.is_dead:
                actual_head_color = DEAD_SNAKE_COLOR
            elif self.is_starving:
                # Starving heads get a brighter pulse effect
                pulse = int(128 + 127 * math.sin(time.time() * 8))
                if self.is_hunter:
                    actual_head_color = (255, pulse//2, 0)  # Bright orange pulse for starving hunters
                else:
                    actual_head_color = (255, pulse, 0)  # Bright yellow pulse for starving normal snakes
            else:
                # Check for active effects on head
                actual_head_color = self.head_color
                for effect in effects:
                    if effect.effect_type == "immunity":
                        # Golden pulsing effect for immunity
                        immunity_pulse = int(150 + 105 * math.sin(time.time() * IMMUNITY_FOOD_FLASH_SPEED))
                        actual_head_color = (immunity_pulse, max(0, immunity_pulse - 50), 0)
                        break
                    elif effect.effect_type == "speed_boost":
                        # Bright cyan for speed boost
                        speed_pulse = int(100 + 100 * math.sin(time.time() * 15))
                        actual_head_color = (speed_pulse, 255, 255)
                        break
                    elif effect.effect_type == "slow":
                        # Dark purple for slow effect
                        actual_head_color = (128, 0, 128)
                        break
                
            pygame.draw.circle(screen, actual_head_color, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for head
            inner_head_detail = (max(0,actual_head_color[0]-30), max(0,actual_head_color[1]-30), max(0,actual_head_color[2]-30))
            pygame.draw.circle(screen, inner_head_detail, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

            # Draw special effect auras around the head
            for effect in effects:
                if effect.effect_type == "immunity":
                    # Golden aura around immune snakes
                    aura_radius = SNAKE_SEGMENT_RADIUS + 8 + int(3 * math.sin(time.time() * 6))
                    aura_alpha = int(100 + 50 * math.sin(time.time() * 4))
                    aura_color = (255, 215, 0, aura_alpha)
                    aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(aura_surface, aura_color, (aura_radius, aura_radius), aura_radius, 3)
                    screen.blit(aura_surface, (head_draw_pos.x - aura_radius, head_draw_pos.y - aura_radius))
                    
                elif effect.effect_type == "speed_boost":
                    # Speed lines around fast snakes
                    for i in range(6):
                        angle = time.time() * 15 + i * 60
                        line_length = SNAKE_SEGMENT_RADIUS + 12
                        end_x = head_draw_pos.x + line_length * math.cos(math.radians(angle))
                        end_y = head_draw_pos.y + line_length * math.sin(math.radians(angle))
                        line_color = (0, 255, 255, 150)
                        line_surface = pygame.Surface((3, int(line_length * 2)), pygame.SRCALPHA)
                        pygame.draw.line(line_surface, line_color, (1, int(line_length)), (1, int(line_length * 1.5)), 2)
                        # Rotate and blit the line (simplified approach)
                        pygame.draw.line(screen, (0, 255, 255), 
                                       (int(head_draw_pos.x), int(head_draw_pos.y)),
                                       (int(end_x), int(end_y)), 2)

            # Draw eyes on the head if not dead
            if not self.is_dead and self.velocity.length_squared() > 0:
                direction_vector = self.velocity.normalize()
                perp_vector = Vector2(-direction_vector.y, direction_vector.x) * (SNAKE_SEGMENT_RADIUS * 0.4)
                eye_offset_forward = direction_vector * (SNAKE_SEGMENT_RADIUS * 0.3)

                eye1_pos = head_draw_pos + eye_offset_forward + perp_vector
                eye2_pos = head_draw_pos + eye_offset_forward - perp_vector

                eye_radius = SNAKE_SEGMENT_RADIUS * 0.25 # Slightly larger eyes
                pupil_radius = eye_radius * 0.5

                pygame.draw.circle(screen, (255,255,255), (int(eye1_pos.x), int(eye1_pos.y)), int(eye_radius))
                pygame.draw.circle(screen, (255,255,255), (int(eye2_pos.x), int(eye2_pos.y)), int(eye_radius))
                pygame.draw.circle(screen, (0,0,0), (int(eye1_pos.x), int(eye1_pos.y)), int(pupil_radius))
                pygame.draw.circle(screen, (0,0,0), (int(eye2_pos.x), int(eye2_pos.y)), int(pupil_radius))            # Draw health bar above snake head if not at full health or dead
            if not self.is_dead and self.hp < self.max_hp:
                health_bar_width = SNAKE_SEGMENT_RADIUS * 4  # Made wider
                health_bar_height = 6  # Made taller
                health_bar_x = head_draw_pos.x - health_bar_width // 2
                health_bar_y = head_draw_pos.y - SNAKE_SEGMENT_RADIUS - 15  # Moved further up
                
                # Background (dark red)
                pygame.draw.rect(screen, (80, 0, 0), 
                               (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
                
                # Health bar (green to red gradient based on health)
                health_percentage = self.get_health_percentage()
                current_health_width = int((health_percentage / 100) * health_bar_width)
                
                if health_percentage > 60:
                    health_color = (0, 255, 0)  # Green
                elif health_percentage > 30:
                    health_color = (255, 255, 0)  # Yellow
                else:
                    health_color = (255, 0, 0)  # Red
                    
                if current_health_width > 0:
                    pygame.draw.rect(screen, health_color,
                                   (health_bar_x, health_bar_y, current_health_width, health_bar_height))
                
                # Health bar border (white for visibility)
                pygame.draw.rect(screen, (255, 255, 255),
                               (health_bar_x - 1, health_bar_y - 1, health_bar_width + 2, health_bar_height + 2), 1)
                
                # Debug: HP text above health bar
                hp_text = f"{self.hp:.1f}/{self.max_hp}"
                if hasattr(self, '_debug_font'):
                    font = self._debug_font
                else:
                    font = pygame.font.Font(None, 16)
                    self._debug_font = font
                    
                text_surface = font.render(hp_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.centerx = head_draw_pos.x
                text_rect.bottom = health_bar_y - 2
                screen.blit(text_surface, text_rect)
