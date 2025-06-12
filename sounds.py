import pygame.mixer as mix
import pygame

import numpy as np

mix.init(frequency=22050, size=-16, channels=2, buffer=512)

sound_cooldowns = {
            'food_eat': 0.1,
            'snake_death': 0.5,
            'black_hole_spawn': 1.0,
            'ripper_spawn': 1.0,
            'scavenger_spawn': 1.0,
            'speed_zone_enter': 0.2,
            'speed_zone_exit': 0.2,
            'black_hole_consume': 0.3,
            'food_magnet_attract': 0.05,
            'effect_expire': 0.5,
            'starvation_warning': 1.0,
            'starvation_critical': 0.5,
            'ripper_kill_hunter': 0.3,
            'creature_despawn': 0.3,
            'snake_spawn': 0.2,
            'food_spawn': 0.02,
            'game_ambient': 5.0,
        }

pygame.sndarray.make_sound(np.zeros((1, 2), dtype=np.int16))