# resource_manager_optimized.py: Enhanced resource management with performance optimizations
import time
import gc
import arcade
from collections import deque, OrderedDict


class OptimizedTextCache:
    """LRU Cache for pre-rendered text objects with enhanced performance"""

    def __init__(self, max_size=150):
        self.max_size = max_size
        self.cached_texts = (
            OrderedDict()
        )  # Key: (text, size, color) -> Value: Text object
        self.cache_hits = 0
        self.cache_misses = 0

    def get_text(self, text_str, size, color):
        """Get cached text object or create new one using LRU caching strategy"""
        key = (text_str, size, tuple(color) if isinstance(color, list) else color)

        if key in self.cached_texts:
            # Move to end (most recently used)
            self.cache_hits += 1
            self.cached_texts.move_to_end(key)
            return self.cached_texts[key]

        # Create new text object
        try:
            text_obj = arcade.Text(text_str, x=0, y=0, color=color, font_size=size)

            # If cache is full, remove least recently used item
            if len(self.cached_texts) >= self.max_size:
                self.cached_texts.popitem(last=False)

            self.cached_texts[key] = text_obj
            self.cache_misses += 1
            return text_obj
        except:
            # Fallback if Text object creation fails
            return None

    def get_cache_stats(self):
        """Get cache performance statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "hit_rate": hit_rate,
            "cache_size": len(self.cached_texts),
            "hits": self.cache_hits,
            "misses": self.cache_misses,
        }


class NumpyParticleSystem:
    """High-performance particle system using NumPy vectorization"""

    def __init__(self, max_particles=1000):
        import numpy as np

        # Pre-allocate arrays for particle properties
        self.positions = np.zeros((max_particles, 2), dtype=np.float32)
        self.velocities = np.zeros((max_particles, 2), dtype=np.float32)
        self.colors = np.zeros((max_particles, 4), dtype=np.uint8)  # RGBA
        self.sizes = np.ones(max_particles, dtype=np.float32)
        self.lifetimes = np.ones(max_particles, dtype=np.float32)
        self.ages = np.zeros(max_particles, dtype=np.float32)
        self.active = np.zeros(max_particles, dtype=bool)

        self.max_particles = max_particles
        self.active_count = 0
        self.next_index = 0
        self.total_created = 0
        self.np = np

    def create_particle(
        self, x, y, vx=0, vy=0, color=(255, 255, 255, 255), size=1.0, lifetime=1.0
    ):
        """Create a new particle or recycle an existing one"""

        # Find an available slot - first try the next index
        idx = self.next_index

        # If that slot is active, find another one
        if self.active[idx]:
            # Find the first inactive slot
            inactive = self.np.where(~self.active)[0]
            if len(inactive) > 0:
                idx = inactive[0]
            else:
                # All slots are active, replace the oldest one
                oldest_idx = self.np.argmax(self.ages)
                idx = oldest_idx

        # Set particle properties
        self.positions[idx] = [x, y]
        self.velocities[idx] = [vx, vy]
        self.colors[idx] = color
        self.sizes[idx] = size
        self.lifetimes[idx] = lifetime
        self.ages[idx] = 0
        self.active[idx] = True

        self.total_created += 1
        self.active_count = self.np.sum(self.active)
        self.next_index = (idx + 1) % self.max_particles

        return idx

    def update(self, dt):
        """Update all active particles simultaneously using vectorized operations"""
        if self.active_count == 0:
            return

        # Update only active particles
        active_mask = self.active

        # Update ages
        self.ages[active_mask] += dt

        # Apply physics
        self.positions[active_mask] += self.velocities[active_mask] * dt

        # Deactivate expired particles
        expired = (self.ages > self.lifetimes) & active_mask
        self.active[expired] = False
        self.active_count = self.np.sum(self.active)

    def draw(self, arcade_window):
        """Draw all active particles"""
        # Create a list of parameters for batch drawing
        draw_list = []

        # Only process active particles
        active_indices = self.np.where(self.active)[0]
        for i in active_indices:
            x, y = self.positions[i]
            size = self.sizes[i]
            color = tuple(self.colors[i])

            # Add to draw list
            draw_list.append((x, y, size, color))

        # Use batch drawing for better performance
        for x, y, size, color in draw_list:
            arcade.draw_circle_filled(x, y, size, color)

    def get_performance_stats(self):
        """Get particle system statistics"""
        return {
            "active": self.active_count,
            "capacity": self.max_particles,
            "utilization": (self.active_count / self.max_particles) * 100,
            "total_created": self.total_created,
        }


class OptimizedObjectPool:
    """Enhanced object pool with better memory management and performance monitoring"""

    def __init__(self, factory_func, reset_func, initial_size=20, max_size=100):
        self.factory_func = factory_func
        self.reset_func = reset_func
        self.available_objects = deque()
        self.active_objects = set()
        self.max_size = max_size
        self.total_created = 0
        self.total_reused = 0
        self.last_cleanup = time.time()

        # Pre-populate pool with initial objects
        for _ in range(initial_size):
            obj = self.factory_func()
            self.available_objects.append(obj)
            self.total_created += 1

    def get_object(self, *args, **kwargs):
        """Get an object from the pool with performance tracking"""
        if self.available_objects:
            obj = self.available_objects.popleft()
            self.reset_func(obj, *args, **kwargs)
            self.total_reused += 1
        else:
            obj = self.factory_func(*args, **kwargs)
            self.total_created += 1

        self.active_objects.add(obj)
        return obj

    def return_object(self, obj):
        """Return an object to the pool"""
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            # Only keep objects if under max size
            if len(self.available_objects) < self.max_size:
                self.available_objects.append(obj)

    def cleanup_unused(self, max_idle=30.0):
        """Periodically trim the pool to save memory"""
        current_time = time.time()
        if (
            current_time - self.last_cleanup > max_idle
            and len(self.available_objects) > self.max_size // 2
        ):
            # Trim down to half the max size
            target_size = self.max_size // 2
            while len(self.available_objects) > target_size:
                self.available_objects.pop()
            self.last_cleanup = current_time

    def get_performance_stats(self):
        """Get pool performance statistics"""
        reuse_rate = (
            (self.total_reused / (self.total_created + self.total_reused) * 100)
            if (self.total_created + self.total_reused) > 0
            else 0
        )
        return {
            "active": len(self.active_objects),
            "available": len(self.available_objects),
            "reuse_rate": reuse_rate,
            "total_created": self.total_created,
            "total_reused": self.total_reused,
        }
