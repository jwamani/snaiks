# ui_enhancements.py: Enhanced UI system for SNAIKS
import pygame
import math
import time
from settings import *

class UIManager:
    """Enhanced UI management system for SNAIKS"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initialize Pygame fonts only if Pygame is available and initialized
        try:
            pygame.font.get_init()
            self.font_small = pygame.font.Font(None, 16)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 32)
            self.pygame_available = True
        except (pygame.error, AttributeError):
            # Pygame not available or not initialized - use Arcade mode
            self.font_small = None
            self.font_medium = None
            self.font_large = None
            self.pygame_available = False

        # UI Panel areas
        self.info_panel_width = 200
        self.minimap_size = 150

    def draw_enhanced_hud(self, screen, game_stats):
        """Draw enhanced HUD with survival information"""
        # Background panel
        panel_rect = pygame.Rect(
            self.screen_width - self.info_panel_width,
            0,
            self.info_panel_width,
            self.screen_height,
        )
        panel_surface = pygame.Surface((self.info_panel_width, self.screen_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((20, 20, 20))
        screen.blit(panel_surface, panel_rect)

        # Draw survival statistics
        y_offset = 10
        self._draw_survival_stats(screen, game_stats, y_offset)

        # Draw minimap
        self._draw_minimap(screen, game_stats, y_offset + 200)

        # Draw health legend
        self._draw_health_legend(screen, y_offset + 380)

    def _draw_survival_stats(self, screen, stats, y_offset):
        """Draw survival statistics panel"""
        x = self.screen_width - self.info_panel_width + 10

        # Title
        title = self.font_medium.render("SURVIVAL STATUS", True, (255, 255, 255))
        screen.blit(title, (x, y_offset))
        y_offset += 30

        # Statistics
        stat_items = [
            f"Alive Snakes: {stats.get('alive_snakes', 0)}",
            f"Hunters: {stats.get('hunters', 0)}",
            f"Average HP: {stats.get('avg_hp', 0):.1f}",
            f"Critical Snakes: {stats.get('critical_snakes', 0)}",
            f"Health Food: {stats.get('health_food', 0)}",
            f"Active Hazards: {stats.get('hazards', 0)}",
        ]

        for i, stat in enumerate(stat_items):
            color = (200, 200, 200)
            if "Critical" in stat and stats.get("critical_snakes", 0) > 0:
                color = (255, 100, 100)  # Red for critical
            elif "Hunters" in stat:
                color = (255, 150, 150)  # Light red for hunters

            text = self.font_small.render(stat, True, color)
            screen.blit(text, (x, y_offset + i * 20))

    def _draw_minimap(self, screen, stats, y_offset):
        """Draw minimap showing snake positions and health"""
        x = self.screen_width - self.info_panel_width + 10

        # Minimap background
        minimap_rect = pygame.Rect(x, y_offset, self.minimap_size, self.minimap_size)
        pygame.draw.rect(screen, (40, 40, 40), minimap_rect)
        pygame.draw.rect(screen, (100, 100, 100), minimap_rect, 2)

        # Title
        title = self.font_small.render("MINIMAP", True, (255, 255, 255))
        screen.blit(title, (x, y_offset - 20))

        # Draw snake positions (if stats provided)
        if "snake_positions" in stats:
            for snake_data in stats["snake_positions"]:
                # Scale position to minimap
                map_x = x + (snake_data["x"] / self.screen_width) * self.minimap_size
                map_y = (
                    y_offset
                    + (snake_data["y"] / self.screen_height) * self.minimap_size
                )

                # Color based on health
                health_pct = snake_data.get("health_pct", 100)
                if health_pct > 60:
                    color = (0, 255, 0)  # Green
                elif health_pct > 30:
                    color = (255, 255, 0)  # Yellow
                else:
                    color = (255, 0, 0)  # Red

                pygame.draw.circle(screen, color, (int(map_x), int(map_y)), 2)

    def _draw_health_legend(self, screen, y_offset):
        """Draw health system legend"""
        x = self.screen_width - self.info_panel_width + 10

        # Title
        title = self.font_small.render("HEALTH LEGEND", True, (255, 255, 255))
        screen.blit(title, (x, y_offset))
        y_offset += 25

        # Legend items
        legend_items = [
            ("Healthy (60-100%)", (0, 255, 0)),
            ("Injured (30-60%)", (255, 255, 0)),
            ("Critical (0-30%)", (255, 0, 0)),
            ("Health Food", (255, 100, 100)),
        ]

        for i, (label, color) in enumerate(legend_items):
            # Color indicator
            pygame.draw.rect(screen, color, (x, y_offset + i * 18, 12, 12))
            # Label
            text = self.font_small.render(label, True, (200, 200, 200))
            screen.blit(text, (x + 18, y_offset + i * 18))

    def draw_enhanced_snake_info(self, screen, snake, offset_y=0):
        """Draw enhanced information above snakes"""
        if snake.is_dead:
            return

        head_pos = snake.head_position

        # Health bar (already implemented in snake.py)
        # Additional info for critically injured snakes
        if snake.is_critically_injured():
            # Danger indicator
            danger_radius = 25 + int(5 * math.sin(time.time() * 10))
            danger_color = (255, 0, 0, 100)
            danger_surface = pygame.Surface(
                (danger_radius * 2, danger_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                danger_surface,
                danger_color,
                (danger_radius, danger_radius),
                danger_radius,
                3,
            )
            screen.blit(
                danger_surface, (head_pos.x - danger_radius, head_pos.y - danger_radius)
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
            )  # Count dangerous effects as hazards

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
            "hazards": hazards_count,  # Environmental hazards count
            "snake_positions": snake_positions,
        }

    # ===== ARCADE-COMPATIBLE METHODS =====    
    def draw_enhanced_hud_arcade(self, arcade_window, game_stats, snakes):
        """Draw enhanced HUD using Arcade graphics - PERFORMANCE OPTIMIZED VERSION
        
        NO TEXT RENDERING - Uses visual indicators only for maximum FPS
        """
        import arcade
        
        # PERFORMANCE: Draw minimal UI with NO text rendering
        # Simple status panel with colored indicators only
        
        panel_width = 200
        panel_height = 120
        panel_x = SCREEN_WIDTH - panel_width - 10
        panel_y = SCREEN_HEIGHT - panel_height - 10
        
        # Draw simple panel background
        arcade.draw_lrbt_rectangle_filled(
            panel_x, panel_x + panel_width, panel_y, panel_y + panel_height,
            (0, 0, 0, 150)
        )
        
        # Border
        arcade.draw_lrbt_rectangle_outline(
            panel_x, panel_x + panel_width, panel_y, panel_y + panel_height,
            arcade.color.WHITE, 1
        )
        
        # Visual indicators only (no text)
        # Green dots = alive snakes (max 20 shown)
        alive_count = min(game_stats.get('alive_snakes', 0), 20)
        for i in range(alive_count):
            x_pos = panel_x + 15 + (i % 10) * 15
            y_pos = panel_y + panel_height - 25 - (i // 10) * 15
            arcade.draw_circle_filled(x_pos, y_pos, 3, arcade.color.GREEN)
        
        # Red dots = hunters
        hunter_count = min(game_stats.get('hunters', 0), 10)
        for i in range(hunter_count):
            x_pos = panel_x + 15 + (i % 10) * 15
            y_pos = panel_y + panel_height - 50 - (i // 10) * 15
            arcade.draw_circle_filled(x_pos, y_pos, 3, arcade.color.RED)
        
        # Yellow dots = critical health snakes
        critical_count = min(game_stats.get('critical_snakes', 0), 10)
        for i in range(critical_count):
            x_pos = panel_x + 15 + (i % 10) * 15
            y_pos = panel_y + panel_height - 75 - (i // 10) * 15
            arcade.draw_circle_filled(x_pos, y_pos, 3, arcade.color.YELLOW)
        
        # Health bar representing average health
        avg_hp = game_stats.get('avg_hp', 100)
        health_bar_width = panel_width - 30
        health_bar_height = 8
        health_x = panel_x + 15
        health_y = panel_y + 15
        
        # Health bar background
        arcade.draw_lrbt_rectangle_filled(
            health_x, health_x + health_bar_width, health_y, health_y + health_bar_height,
            (60, 0, 0)
        )
        
        # Health bar fill
        fill_width = (avg_hp / 100) * health_bar_width
        if avg_hp > 60:
            health_color = arcade.color.GREEN
        elif avg_hp > 30:
            health_color = arcade.color.YELLOW
        else:
            health_color = arcade.color.RED
            
        if fill_width > 0:            arcade.draw_lrbt_rectangle_filled(
                health_x, health_x + fill_width, health_y, health_y + health_bar_height,
                health_color
            )

    def draw_enhanced_snake_info_arcade(self, arcade_window, snake):
        """Draw enhanced snake information using Arcade graphics - PERFORMANCE OPTIMIZED
        
        NO TEXT RENDERING - Visual indicators only
        """
        import arcade

        if snake.is_dead or not snake.is_critically_injured():
            return

        # Critical health warning for low-health snakes (visual only)
        head_pos = snake.head_position

        # Simple pulsing warning circle (no text)
        pulse = 0.5 + 0.5 * math.sin(time.time() * 8)
        warning_alpha = int(150 * pulse)

        # Warning circle around critical snake
        arcade.draw_circle_outline(
            head_pos.x, head_pos.y, 25 + 10 * pulse, (255, 0, 0, warning_alpha), 3
        )
        arcade.draw_circle_outline(
            head_pos.x, head_pos.y, 25 + 10 * pulse, (255, 0, 0, warning_alpha), 3
        )    
    def _draw_minimap_arcade(self, arcade_window, snake_positions, x, y):
        """Draw minimap using Arcade graphics - PERFORMANCE OPTIMIZED
        
        NO TEXT RENDERING - Visual indicators only
        """
        import arcade
        
        # Simple minimap background
        arcade.draw_lrbt_rectangle_filled(
            x, x + self.minimap_size, y, y + self.minimap_size, (40, 40, 40, 200)
        )
        
        # Minimap border
        arcade.draw_lrbt_rectangle_outline(
            x, x + self.minimap_size, y, y + self.minimap_size,
            arcade.color.WHITE, 2,
        )

        # Scale factors for minimap
        scale_x = self.minimap_size / self.screen_width
        scale_y = self.minimap_size / self.screen_height

        # Draw snake positions (visual only, no text)
        for snake_data in snake_positions:
            map_x = x + snake_data["x"] * scale_x
            map_y = y + snake_data["y"] * scale_y

            # Color based on health and type
            if snake_data["is_hunter"]:
                color = arcade.color.RED
            elif snake_data["health_pct"] < 30:
                color = arcade.color.ORANGE
            else:
                color = arcade.color.GREEN

            arcade.draw_circle_filled(map_x, map_y, 2, color)

        # NO TEXT TITLE - removed for performance
