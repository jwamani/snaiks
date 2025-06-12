# main_arcade.py: Main game loop with Arcade graphics library
import arcade
import random
from settings import *
from snake import Snake
from food import Food
from game_manager import GameManager

class SnaiksGame(arcade.Window):
    """Main game window using Arcade graphics library"""
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "SNAIKS - Snake Battle Royale", resizable=False)
        
        # Set background color
        self.background_color = arcade.color_from_hex_string("#141E28")  # Convert BG_COLOR to Arcade format
        
        # Initialize game manager
        self.game_manager = GameManager()
        
        # Performance tracking
        self.frame_count = 0
        self.performance_timer = 0
        
        print("🎮 SNAIKS Arcade - Advanced Graphics Mode")
        print(f"📐 Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"⚡ Target FPS: {FPS}")
        print("✨ Enhanced visual effects enabled")
        
    def setup(self):
        """Set up the game"""
        # Additional setup can be done here if needed
        pass
        
    def on_draw(self):
        """Render the game"""
        # Start rendering
        self.clear()
        
        # Draw game elements
        self.game_manager.draw_arcade(self)
        
        # Performance info (optional debug)
        if hasattr(self, 'show_performance') and self.show_performance:
            arcade.draw_text(f"FPS: {int(1/self.delta_time) if self.delta_time > 0 else 0}", 
                           10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
            arcade.draw_text(f"Entities: {len(self.game_manager.snakes) + len(self.game_manager.food_items)}", 
                           10, SCREEN_HEIGHT - 50, arcade.color.WHITE, 16)
        
    def on_update(self, delta_time):
        """Update game logic"""
        # Update game state
        self.game_manager.update()
        
        # Track performance
        self.frame_count += 1
        self.performance_timer += delta_time
        
        # Log performance every 5 seconds
        if self.performance_timer >= 5.0:
            avg_fps = self.frame_count / self.performance_timer
            print(f"⚡ Performance: {avg_fps:.1f} FPS average")
            self.frame_count = 0
            self.performance_timer = 0
            
    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        if key == arcade.key.ESCAPE:
            self.close()
        elif key == arcade.key.F1:
            # Toggle performance display
            self.show_performance = getattr(self, 'show_performance', False)
            self.show_performance = not self.show_performance
        elif key == arcade.key.R:
            # Reset game
            self.game_manager = GameManager()
            print("🔄 Game reset")
        elif key == arcade.key.P:
            # Pause/unpause (if implemented)
            pass
            
    def on_close(self):
        """Handle window closing"""
        print("👋 Thanks for playing SNAIKS!")
        super().on_close()

def main():
    """Main function to start the game"""
    # Create and run the game
    game = SnaiksGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
