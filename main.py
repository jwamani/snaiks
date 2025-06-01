# main.py: Main game loop, Pygame setup, event handling
import pygame
from settings import *
from snake import Snake
from food import Food
from game_manager import GameManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Battle Royale")
    clock = pygame.time.Clock()

    game_manager = GameManager()

    # Start ambient background sound
    import time
    last_ambient_time = time.time()
    ambient_interval = 5.0  # Play ambient sound every 5 seconds

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        # Game logic updates
        game_manager.update()

        # Play ambient sound periodically
        current_time = time.time()
        if current_time - last_ambient_time >= ambient_interval:
            game_manager.sound_manager.play_ambient_sound()
            last_ambient_time = current_time

        # Drawing
        screen.fill(BG_COLOR)
        game_manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()

