# ui_simple.py: High-performance UI system for SNAIKS
# NO TEXT RENDERING - Visual indicators only for maximum FPS

import arcade
import math
import time
from settings import *


class UIManager:
    """High-performance UI management system - NO TEXT RENDERING"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.minimap_size = 100  # Smaller for better performance

    def draw_enhanced_hud_arcade(self, arcade_window, game_stats, snakes):
        """Draw performance-optimized HUD - Visual indicators only"""

        # Simple status panel
        panel_width = 150
        panel_height = 80
        panel_x = SCREEN_WIDTH - panel_width - 10
        panel_y = SCREEN_HEIGHT - panel_height - 10

        # Panel background
        arcade.draw_lrbt_rectangle_filled(
            panel_x,
            panel_x + panel_width,
            panel_y,
            panel_y + panel_height,
            (0, 0, 0, 120),
        )

        # Border
        arcade.draw_lrbt_rectangle_outline(
            panel_x,
            panel_x + panel_width,
            panel_y,
            panel_y + panel_height,
            arcade.color.WHITE,
            1,
        )

        # Visual indicators (no text)
        # Green dots = alive snakes
        alive_count = min(game_stats.get("alive_snakes", 0), 15)
        for i in range(alive_count):
            x_pos = panel_x + 10 + (i % 10) * 12
            y_pos = panel_y + panel_height - 20 - (i // 10) * 12
            arcade.draw_circle_filled(x_pos, y_pos, 2, arcade.color.GREEN)

        # Red dots = hunters
        hunter_count = min(game_stats.get("hunters", 0), 10)
        for i in range(hunter_count):
            x_pos = panel_x + 10 + (i % 10) * 12
            y_pos = panel_y + panel_height - 40 - (i // 10) * 12
            arcade.draw_circle_filled(x_pos, y_pos, 2, arcade.color.RED)

        # Average health bar
        avg_hp = game_stats.get("avg_hp", 100)
        health_bar_width = panel_width - 20
        health_bar_height = 6
        health_x = panel_x + 10
        health_y = panel_y + 10

        # Health bar background
        arcade.draw_lrbt_rectangle_filled(
            health_x,
            health_x + health_bar_width,
            health_y,
            health_y + health_bar_height,
            (60, 0, 0),
        )

        # Health bar fill
        fill_width = (avg_hp / 100) * health_bar_width
        health_color = (
            arcade.color.GREEN
            if avg_hp > 60
            else (arcade.color.YELLOW if avg_hp > 30 else arcade.color.RED)
        )

        if fill_width > 0:
            arcade.draw_lrbt_rectangle_filled(
                health_x,
                health_x + fill_width,
                health_y,
                health_y + health_bar_height,
                health_color,
            )

    def draw_enhanced_snake_info_arcade(self, arcade_window, snake):
        """Draw critical snake warning - Visual only"""
        if snake.is_dead or not snake.is_critically_injured():
            return

        head_pos = snake.head_position

        # Simple pulsing warning circle (no text)
        pulse = 0.5 + 0.5 * math.sin(time.time() * 8)
        warning_alpha = int(100 * pulse)

        arcade.draw_circle_outline(
            head_pos.x, head_pos.y, 20 + 8 * pulse, (255, 0, 0, warning_alpha), 2
        )

    def get_game_stats(self, snakes, food_items, effects_manager=None):
        """Calculate game statistics for UI display"""
        alive_snakes = [s for s in snakes if not s.is_dead]
        hunters = [s for s in alive_snakes if s.is_hunter]
        critical_snakes = [s for s in alive_snakes if s.is_critically_injured()]
        health_food = [f for f in food_items if f.food_type == "health"]

        total_hp = sum(s.hp for s in alive_snakes)
        avg_hp = total_hp / len(alive_snakes) if alive_snakes else 0

        # Count environmental hazards
        hazards_count = 0
        if effects_manager:
            effect_counts = effects_manager.get_effect_counts()
            hazards_count = effect_counts.get("poison_zones", 0) + effect_counts.get(
                "black_holes", 0
            )

        snake_positions = []
        for snake in alive_snakes:
            snake_positions.append(
                {
                    "x": snake.head_position.x,
                    "y": snake.head_position.y,
                    "health_pct": snake.get_health_percentage(),
                    "is_hunter": snake.is_hunter,
                }
            )

        return {
            "alive_snakes": len(alive_snakes),
            "hunters": len(hunters),
            "avg_hp": avg_hp,
            "critical_snakes": len(critical_snakes),
            "health_food": len(health_food),
            "hazards": hazards_count,
            "snake_positions": snake_positions,
        }

    def draw_enhanced_hud(self, screen, game_stats):
        """Draw performance-optimized HUD for pygame - Visual indicators only"""
        import pygame

        # Simple status panel
        panel_width = 150
        panel_height = 80
        panel_x = SCREEN_WIDTH - panel_width - 10
        panel_y = SCREEN_HEIGHT - panel_height - 10

        # Panel background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 120))
        screen.blit(panel_surface, (panel_x, panel_y))

        # Border
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (panel_x, panel_y, panel_width, panel_height),
            1,
        )

        # Visual indicators (no text)
        # Green dots = alive snakes
        alive_count = min(game_stats.get("alive_snakes", 0), 15)
        for i in range(alive_count):
            x_pos = panel_x + 10 + (i % 10) * 12
            y_pos = panel_y + 20 + (i // 10) * 12
            pygame.draw.circle(screen, (0, 255, 0), (x_pos, y_pos), 2)

        # Red dots = hunters
        hunter_count = min(game_stats.get("hunters", 0), 10)
        for i in range(hunter_count):
            x_pos = panel_x + 10 + (i % 10) * 12
            y_pos = panel_y + 40 + (i // 10) * 12
            pygame.draw.circle(screen, (255, 0, 0), (x_pos, y_pos), 2)

        # Average health bar
        avg_hp = game_stats.get("avg_hp", 100)
        health_bar_width = panel_width - 20
        health_bar_height = 6
        health_x = panel_x + 10
        health_y = panel_y + panel_height - 20

        # Health bar background
        pygame.draw.rect(
            screen,
            (60, 0, 0),
            (health_x, health_y, health_bar_width, health_bar_height),
        )

        # Health bar fill
        fill_width = int((avg_hp / 100) * health_bar_width)
        if avg_hp > 60:
            health_color = (0, 255, 0)
        elif avg_hp > 30:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)

        if fill_width > 0:
            pygame.draw.rect(
                screen,
                health_color,
                (health_x, health_y, fill_width, health_bar_height),
            )

    def draw_enhanced_snake_info(self, screen, snake):
        """Draw critical snake warning for pygame - Visual only"""
        import pygame
        import math
        import time

        if snake.is_dead or not snake.is_critically_injured():
            return

        head_pos = snake.head_position

        # Simple pulsing warning circle (no text)
        pulse = 0.5 + 0.5 * math.sin(time.time() * 8)
        warning_alpha = int(100 * pulse)
        warning_radius = int(20 + 8 * pulse)

        # Create a surface for the warning circle with alpha
        warning_surface = pygame.Surface(
            (warning_radius * 2, warning_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            warning_surface,
            (255, 0, 0, warning_alpha),
            (warning_radius, warning_radius),
            warning_radius,
            2,
        )
        screen.blit(
            warning_surface,
            (head_pos.x - warning_radius, head_pos.y - warning_radius),
        )
