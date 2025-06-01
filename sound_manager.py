# sound_manager.py: Sound effects management for game events
import pygame
import math
import numpy as np
from settings import *
import time

class SoundManager:
    """Manages all sound effects in the game"""
    
    def __init__(self):
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.enabled = ENABLE_SOUND_EFFECTS
        self.sounds = {}
        self.last_sound_times = {}  # Prevent sound spam        
        self.sound_cooldowns = {
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
        
        if self.enabled:
            self._generate_sounds()
            print("SoundManager initialized with generated sound effects")
        else:
            print("SoundManager initialized but sound effects are disabled")
    
    def _generate_sounds(self):
        """Generate sound effects programmatically using pygame and numpy"""
        try:
            # Snake eating food sounds
            self.sounds['food_eat_normal'] = self._generate_eat_sound(440, 0.1, 'normal')
            self.sounds['food_eat_speed'] = self._generate_eat_sound(660, 0.1, 'speed')
            self.sounds['food_eat_slow'] = self._generate_eat_sound(220, 0.15, 'slow')
            self.sounds['food_eat_immunity'] = self._generate_eat_sound(880, 0.1, 'immunity')
            self.sounds['food_eat_growth'] = self._generate_eat_sound(330, 0.2, 'growth')
            self.sounds['food_eat_shrink'] = self._generate_eat_sound(110, 0.2, 'shrink')
            
            # Snake death sounds
            self.sounds['snake_death_starvation'] = self._generate_death_sound('starvation')
            self.sounds['snake_death_eaten'] = self._generate_death_sound('eaten')
            self.sounds['snake_death_ripper'] = self._generate_death_sound('ripper')
            self.sounds['snake_death_wall'] = self._generate_death_sound('wall')
            
            # Snake transformation
            self.sounds['snake_become_hunter'] = self._generate_transformation_sound()
            
            # Environmental effects
            self.sounds['black_hole_spawn'] = self._generate_black_hole_spawn_sound()
            self.sounds['black_hole_pull'] = self._generate_black_hole_pull_sound()
            self.sounds['speed_zone_spawn'] = self._generate_speed_zone_sound()
            self.sounds['food_magnet_spawn'] = self._generate_food_magnet_sound()
            
            # Creature sounds
            self.sounds['ripper_spawn'] = self._generate_ripper_spawn_sound()
            self.sounds['ripper_attack'] = self._generate_ripper_attack_sound()
            self.sounds['scavenger_spawn'] = self._generate_scavenger_spawn_sound()
            self.sounds['scavenger_steal'] = self._generate_scavenger_steal_sound()
              # Effect activation sounds
            self.sounds['speed_boost_activate'] = self._generate_effect_sound('speed_boost')
            self.sounds['slow_activate'] = self._generate_effect_sound('slow')
            self.sounds['immunity_activate'] = self._generate_effect_sound('immunity')
            
            # Environmental interaction sounds
            self.sounds['speed_zone_enter'] = self._generate_zone_enter_sound()
            self.sounds['speed_zone_exit'] = self._generate_zone_exit_sound()
            self.sounds['black_hole_consume'] = self._generate_black_hole_consume_sound()
            self.sounds['food_magnet_attract'] = self._generate_food_magnet_attract_sound()
            self.sounds['effect_expire'] = self._generate_effect_expire_sound()
            
            # Starvation system sounds
            self.sounds['starvation_warning'] = self._generate_starvation_warning_sound()
            self.sounds['starvation_critical'] = self._generate_starvation_critical_sound()
            
            # Creature interaction sounds
            self.sounds['ripper_kill_hunter'] = self._generate_ripper_kill_sound()
            self.sounds['creature_despawn'] = self._generate_creature_despawn_sound()
            
            # General game event sounds
            self.sounds['snake_spawn'] = self._generate_snake_spawn_sound()
            self.sounds['food_spawn'] = self._generate_food_spawn_sound()
            self.sounds['game_ambient'] = self._generate_ambient_sound()
            
        except Exception as e:
            print(f"Warning: Failed to generate some sounds: {e}")
            self.enabled = False
    
    def _generate_tone(self, frequency, duration, sample_rate=22050, wave_type='sine'):
        """Generate a basic tone"""
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            time_point = float(i) / sample_rate
            if wave_type == 'sine':
                arr[i] = math.sin(2 * math.pi * frequency * time_point)
            elif wave_type == 'square':
                arr[i] = 1 if math.sin(2 * math.pi * frequency * time_point) > 0 else -1
            elif wave_type == 'sawtooth':
                arr[i] = 2 * (time_point * frequency - math.floor(time_point * frequency + 0.5))
        
        # Apply envelope to prevent clicks
        fade_frames = min(100, frames // 10)
        for i in range(fade_frames):
            arr[i] *= i / fade_frames
            arr[frames - 1 - i] *= i / fade_frames
        
        # Convert to 16-bit integers
        arr = (arr * 32767).astype(np.int16)
        
        # Make stereo
        stereo_arr = np.zeros((frames, 2), dtype=np.int16)
        stereo_arr[:, 0] = arr
        stereo_arr[:, 1] = arr
        
        return pygame.sndarray.make_sound(stereo_arr)
    
    def _generate_eat_sound(self, base_freq, duration, food_type):
        """Generate eating sound for different food types"""
        if food_type == 'normal':
            return self._generate_tone(base_freq, duration, wave_type='sine')
        elif food_type == 'speed':
            # Rising pitch for speed food
            return self._generate_sweep_sound(base_freq, base_freq * 1.5, duration)
        elif food_type == 'slow':
            # Falling pitch for slow food
            return self._generate_sweep_sound(base_freq, base_freq * 0.7, duration)
        elif food_type == 'immunity':
            # Bright chime for immunity
            return self._generate_chord_sound([base_freq, base_freq * 1.25, base_freq * 1.5], duration)
        elif food_type == 'growth':
            # Deep growing sound
            return self._generate_sweep_sound(base_freq, base_freq * 0.5, duration)
        elif food_type == 'shrink':
            # High shrinking sound
            return self._generate_sweep_sound(base_freq, base_freq * 2, duration)
        else:
            return self._generate_tone(base_freq, duration)
    
    def _generate_sweep_sound(self, start_freq, end_freq, duration):
        """Generate a frequency sweep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            time_point = float(i) / sample_rate
            progress = time_point / duration
            freq = start_freq + (end_freq - start_freq) * progress
            arr[i] = math.sin(2 * math.pi * freq * time_point)
        
        # Apply envelope
        fade_frames = min(100, frames // 10)
        for i in range(fade_frames):
            arr[i] *= i / fade_frames
            arr[frames - 1 - i] *= i / fade_frames
        
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.zeros((frames, 2), dtype=np.int16)
        stereo_arr[:, 0] = arr
        stereo_arr[:, 1] = arr
        
        return pygame.sndarray.make_sound(stereo_arr)
    
    def _generate_chord_sound(self, frequencies, duration):
        """Generate a chord with multiple frequencies"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for freq in frequencies:
            for i in range(frames):
                time_point = float(i) / sample_rate
                arr[i] += math.sin(2 * math.pi * freq * time_point) / len(frequencies)
        
        # Apply envelope
        fade_frames = min(100, frames // 10)
        for i in range(fade_frames):
            arr[i] *= i / fade_frames
            arr[frames - 1 - i] *= i / fade_frames
        
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.zeros((frames, 2), dtype=np.int16)
        stereo_arr[:, 0] = arr
        stereo_arr[:, 1] = arr
        
        return pygame.sndarray.make_sound(stereo_arr)
    
    def _generate_death_sound(self, death_type):
        """Generate death sounds for different causes"""
        if death_type == 'starvation':
            # Fading weak tone
            return self._generate_sweep_sound(440, 220, 0.5)
        elif death_type == 'eaten':
            # Chomp sound
            return self._generate_tone(150, 0.2, wave_type='square')
        elif death_type == 'ripper':
            # Sharp attack sound
            return self._generate_sweep_sound(800, 200, 0.3)
        elif death_type == 'wall':
            # Impact sound
            return self._generate_tone(100, 0.1, wave_type='square')
        else:
            return self._generate_tone(330, 0.3)
    
    def _generate_transformation_sound(self):
        """Generate sound for snake becoming hunter"""
        # Ascending powerful chord
        return self._generate_chord_sound([220, 330, 440, 660], 0.4)
    
    def _generate_black_hole_spawn_sound(self):
        """Generate black hole spawn sound"""
        # Deep rumbling with sweep
        return self._generate_sweep_sound(60, 120, 0.8)
    
    def _generate_black_hole_pull_sound(self):
        """Generate black hole pulling sound"""
        # Whoosh effect
        return self._generate_sweep_sound(200, 80, 0.3)
    
    def _generate_speed_zone_sound(self):
        """Generate speed zone spawn sound"""
        # Energetic rising tone
        return self._generate_sweep_sound(440, 880, 0.3)
    
    def _generate_food_magnet_sound(self):
        """Generate food magnet spawn sound"""
        # Magnetic humming
        return self._generate_tone(660, 0.4, wave_type='sine')
    
    def _generate_ripper_spawn_sound(self):
        """Generate ripper spawn sound"""
        # Aggressive growl
        return self._generate_tone(120, 0.5, wave_type='square')
    
    def _generate_ripper_attack_sound(self):
        """Generate ripper attack sound"""
        # Sharp aggressive attack
        return self._generate_sweep_sound(600, 200, 0.2)
    
    def _generate_scavenger_spawn_sound(self):
        """Generate scavenger spawn sound"""
        # Bird-like caw
        return self._generate_sweep_sound(800, 400, 0.3)
    
    def _generate_scavenger_steal_sound(self):
        """Generate scavenger stealing food sound"""
        # Quick snatch sound
        return self._generate_tone(550, 0.15, wave_type='square')
    def _generate_effect_sound(self, effect_type):
        """Generate sound for effect activation"""
        if effect_type == 'speed_boost':
            return self._generate_sweep_sound(440, 880, 0.2)
        elif effect_type == 'slow':
            return self._generate_sweep_sound(440, 220, 0.3)
        elif effect_type == 'immunity':
            return self._generate_chord_sound([660, 880, 1100], 0.25)
        else:
            return self._generate_tone(440, 0.2)
    
    def _generate_zone_enter_sound(self):
        """Generate sound for entering speed zones"""
        # Whoosh effect when entering zone
        return self._generate_sweep_sound(300, 600, 0.15)
    
    def _generate_zone_exit_sound(self):
        """Generate sound for exiting speed zones"""
        # Reverse whoosh effect when exiting zone
        return self._generate_sweep_sound(600, 300, 0.15)
    
    def _generate_black_hole_consume_sound(self):
        """Generate sound for entities being consumed by black holes"""
        # Deep distortion effect
        return self._generate_sweep_sound(400, 80, 0.4)
    
    def _generate_food_magnet_attract_sound(self):
        """Generate sound for food being attracted by magnets"""
        # Subtle magnetic pull sound
        return self._generate_tone(480, 0.08, wave_type='sine')
    
    def _generate_effect_expire_sound(self):
        """Generate sound for when environmental effects expire"""
        # Fading chime
        return self._generate_sweep_sound(660, 330, 0.3)
    
    def _generate_starvation_warning_sound(self):
        """Generate warning sound when starvation begins"""
        # Urgent warning beep
        return self._generate_tone(800, 0.1, wave_type='square')
    
    def _generate_starvation_critical_sound(self):
        """Generate critical warning sound as starvation progresses"""
        # Higher pitch, more urgent
        return self._generate_tone(1000, 0.08, wave_type='square')
    
    def _generate_ripper_kill_sound(self):
        """Generate sound when ripper successfully kills a hunter"""
        # Powerful attack sound
        return self._generate_sweep_sound(800, 150, 0.3)
    
    def _generate_creature_despawn_sound(self):
        """Generate sound when creatures despawn or die"""
        # Fading disappearance sound
        return self._generate_sweep_sound(500, 200, 0.5)
    
    def _generate_snake_spawn_sound(self):
        """Generate sound when new snakes spawn"""
        # Gentle birth/appearance sound
        return self._generate_sweep_sound(220, 440, 0.2)
    
    def _generate_food_spawn_sound(self):
        """Generate sound when food spawns"""
        # Light pop sound
        return self._generate_tone(660, 0.05, wave_type='sine')
    
    def _generate_ambient_sound(self):
        """Generate ambient background sound"""
        # Subtle ambient tone
        return self._generate_tone(110, 0.8, wave_type='sine')
    
    def _can_sound(self, sound_name):
        """Check if enough time has passed to play this sound again"""
        if not self.enabled:
            return False
        
        current_time = time.time()
        cooldown = self.sound_cooldowns.get(sound_name, 0.05)  # Default 50ms cooldown
        
        last_time = self.last_sound_times.get(sound_name, 0)
        if current_time - last_time >= cooldown:
            self.last_sound_times[sound_name] = current_time
            return True
        return False
    def play_sound(self, sound_name, volume=0.3):
        """Play a sound effect with volume control"""
        if not self.enabled or not self._can_sound(sound_name):
            return
        
        if sound_name in self.sounds:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(min(1.0, max(0.0, volume)))
                sound.play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    # Convenience methods for game events
    def play_food_eat_sound(self, food_type):
        """Play appropriate eating sound for food type"""
        sound_name = f'food_eat_{food_type}'
        self.play_sound(sound_name, volume=0.2)
    
    def play_snake_death_sound(self, death_reason):
        """Play appropriate death sound for death reason"""
        if death_reason in ['starvation', 'eaten by hunter', 'killed by ripper', 'hit wall']:
            death_type = death_reason.split()[0] if ' ' in death_reason else death_reason
            if death_type == 'eaten':
                death_type = 'eaten'
            elif death_type == 'killed':
                death_type = 'ripper'
            elif death_type == 'hit':
                death_type = 'wall'
            
            sound_name = f'snake_death_{death_type}'
            self.play_sound(sound_name, volume=0.4)
    
    def play_hunter_transformation_sound(self):
        """Play snake becoming hunter sound"""
        self.play_sound('snake_become_hunter', volume=0.5)
    
    def play_black_hole_spawn_sound(self):
        """Play black hole spawn sound"""
        self.play_sound('black_hole_spawn', volume=0.6)
    
    def play_black_hole_pull_sound(self):
        """Play black hole pulling sound"""
        self.play_sound('black_hole_pull', volume=0.3)
    
    def play_speed_zone_spawn_sound(self):
        """Play speed zone spawn sound"""
        self.play_sound('speed_zone_spawn', volume=0.4)
    
    def play_food_magnet_spawn_sound(self):
        """Play food magnet spawn sound"""
        self.play_sound('food_magnet_spawn', volume=0.4)
    
    def play_ripper_spawn_sound(self):
        """Play ripper spawn sound"""
        self.play_sound('ripper_spawn', volume=0.5)
    
    def play_ripper_attack_sound(self):
        """Play ripper attack sound"""
        self.play_sound('ripper_attack', volume=0.6)
    
    def play_scavenger_spawn_sound(self):
        """Play scavenger spawn sound"""
        self.play_sound('scavenger_spawn', volume=0.4)
    
    def play_scavenger_steal_sound(self):
        """Play scavenger stealing food sound"""
        self.play_sound('scavenger_steal', volume=0.3)
    def play_effect_activation_sound(self, effect_type):
        """Play effect activation sound"""
        sound_name = f'{effect_type}_activate'
        self.play_sound(sound_name, volume=0.3)
    
    def play_speed_zone_enter_sound(self):
        """Play sound for entering speed zones"""
        self.play_sound('speed_zone_enter', volume=0.2)
    
    def play_speed_zone_exit_sound(self):
        """Play sound for exiting speed zones"""
        self.play_sound('speed_zone_exit', volume=0.2)
    
    def play_black_hole_consume_sound(self):
        """Play sound for entities being consumed by black holes"""
        self.play_sound('black_hole_consume', volume=0.4)
    
    def play_food_magnet_attract_sound(self):
        """Play sound for food being attracted by magnets"""
        self.play_sound('food_magnet_attract', volume=0.1)
    
    def play_effect_expire_sound(self):
        """Play sound for when environmental effects expire"""
        self.play_sound('effect_expire', volume=0.3)
    
    def play_starvation_warning_sound(self):
        """Play warning sound when starvation begins"""
        self.play_sound('starvation_warning', volume=0.3)
    
    def play_starvation_critical_sound(self):
        """Play critical warning sound as starvation progresses"""
        self.play_sound('starvation_critical', volume=0.4)
    
    def play_ripper_kill_hunter_sound(self):
        """Play sound when ripper successfully kills a hunter"""
        self.play_sound('ripper_kill_hunter', volume=0.5)
    
    def play_creature_despawn_sound(self):
        """Play sound when creatures despawn or die"""
        self.play_sound('creature_despawn', volume=0.3)
    
    def play_snake_spawn_sound(self):
        """Play sound when new snakes spawn"""
        self.play_sound('snake_spawn', volume=0.2)
    
    def play_food_spawn_sound(self):
        """Play sound when food spawns"""
        self.play_sound('food_spawn', volume=0.1)
    
    def play_ambient_sound(self):
        """Play ambient background sound"""
        self.play_sound('game_ambient', volume=0.05)
    
    def set_enabled(self, enabled):
        """Enable or disable sound effects"""
        self.enabled = enabled
        if enabled:
            print("Sound effects enabled")
        else:
            print("Sound effects disabled")
    
    def cleanup(self):
        """Clean up sound resources"""
        if self.sounds:
            self.sounds.clear()
