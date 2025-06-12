# ui_enhancements.py: Enhanced UI system for SNAIKS
import pygame
import math
import time

class UIManager:
    """Enhanced UI management system for SNAIKS"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_small = pygame.font.Font(None, 16)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        # UI Panel areas
        self.info_panel_width = 200
        self.minimap_size = 150
        
    def draw_enhanced_hud(self, screen, game_stats):
        """Draw enhanced HUD with survival information"""
        # Background panel
        panel_rect = pygame.Rect(self.screen_width - self.info_panel_width, 0, 
                               self.info_panel_width, self.screen_height)
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
            if "Critical" in stat and stats.get('critical_snakes', 0) > 0:
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
        if 'snake_positions' in stats:
            for snake_data in stats['snake_positions']:
                # Scale position to minimap
                map_x = x + (snake_data['x'] / self.screen_width) * self.minimap_size
                map_y = y_offset + (snake_data['y'] / self.screen_height) * self.minimap_size
                
                # Color based on health
                health_pct = snake_data.get('health_pct', 100)
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
            danger_surface = pygame.Surface((danger_radius * 2, danger_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(danger_surface, danger_color, (danger_radius, danger_radius), danger_radius, 3)
            screen.blit(danger_surface, (head_pos.x - danger_radius, head_pos.y - danger_radius))
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
            hazards_count = (effect_counts.get('poison_zones', 0) + 
                           effect_counts.get('black_holes', 0))  # Count dangerous effects as hazards
        
        snake_positions = []
        for snake in alive_snakes:
            snake_positions.append({
                'x': snake.head_position.x,
                'y': snake.head_position.y,
                'health_pct': snake.get_health_percentage(),
                'is_hunter': snake.is_hunter
            })
        
        return {
            'alive_snakes': len(alive_snakes),
            'hunters': len(hunters),
            'avg_hp': avg_hp,
            'critical_snakes': len(critical_snakes),
            'health_food': len(health_food),            'hazards': hazards_count,  # Environmental hazards count
            'snake_positions': snake_positions
        }
