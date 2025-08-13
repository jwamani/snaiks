# resource_manager.py:
import time
from collections import deque, OrderedDict
import gc
import arcade


class TextCache:
    """LRU Cache for pre-rendered text objects with enhanced performance"""

    def __init__(self, max_size: int=150):
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

class ObjectPool:
    """Enhanced object pool with performance monitoring"""

    def __init__(self, factory_func, reset_func, initial_size=20, max_size=100):
        self.factory_func = factory_func
        self.reset_func = reset_func
        self.available_objects = deque()
        self.active_objects = set()
        self.max_size = max_size
        self.total_created = 0
        self.total_reused = 0

        # Pre-populate pool with more objects for better performance
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


class PerformanceMonitor:
    """Enhanced performance monitoring with detailed metrics"""

    def __init__(self, window_size=120):  # Increased for better averaging
        self.window_size = window_size
        self.frame_times = deque(maxlen=window_size)
        self.update_times = deque(maxlen=window_size)
        self.draw_times = deque(maxlen=window_size)
        self.collision_times = deque(maxlen=window_size)
        self.last_frame_time = time.time()
        self.last_time = time.time()

    def start_frame(self):
        """Mark the start of a frame"""
        current_time = time.time()
        if hasattr(self, "last_time"):
            frame_time = current_time - self.last_time
            self.frame_times.append(frame_time)
        self.last_time = current_time
        self.frame_start_time = current_time

    def mark_update_time(self):
        """Mark the end of update phase"""
        self.update_end_time = time.time()
        update_time = self.update_end_time - self.frame_start_time
        self.update_times.append(update_time)

    def mark_draw_time(self):
        """Mark the end of draw phase"""
        draw_end_time = time.time()
        draw_time = draw_end_time - self.update_end_time
        self.draw_times.append(draw_time)

    def get_stats(self):
        """Get performance statistics"""
        if not self.frame_times:
            return {}

        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0

        stats = {
            "fps": avg_fps,
            "frame_time_ms": avg_frame_time * 1000,
        }

        if self.update_times:
            avg_update_time = sum(self.update_times) / len(self.update_times)
            stats["update_time_ms"] = avg_update_time * 1000

        if self.draw_times:
            avg_draw_time = sum(self.draw_times) / len(self.draw_times)
            stats["draw_time_ms"] = avg_draw_time * 1000

        return stats


class SpatialGrid:
    """Spatial partitioning for efficient collision detection"""

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = int(width // cell_size) + 1
        self.rows = int(height // cell_size) + 1
        self.clear()

    def clear(self):
        """Clear all objects from the grid"""
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

    def _get_grid_pos(self, x, y):
        """Convert world position to grid coordinates"""
        col = max(0, min(self.cols - 1, int(x // self.cell_size)))
        row = max(0, min(self.rows - 1, int(y // self.cell_size)))
        return col, row

    def add_object(self, obj, x, y):
        """Add object to grid at position"""
        col, row = self._get_grid_pos(x, y)
        self.grid[row][col].append(obj)

    def get_nearby_objects(self, x, y, radius=None):
        """Get objects near the given position"""
        if radius is None:
            radius = self.cell_size

        # Calculate range of cells to check
        min_col = max(0, int((x - radius) // self.cell_size))
        max_col = min(self.cols - 1, int((x + radius) // self.cell_size))
        min_row = max(0, int((y - radius) // self.cell_size))
        max_row = min(self.rows - 1, int((y + radius) // self.cell_size))

        nearby_objects = []
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                nearby_objects.extend(self.grid[row][col])

        return nearby_objects


class ResourceManager:
    """Central resource management system with performance optimizations"""

    def __init__(self):
        self.performance_monitor = PerformanceMonitor()

        # Text rendering cache for optimal performance
        self.text_cache = TextCache()

        # Pool of reusable objects for memory efficiency
        self._init_object_pools()

        # Initialize spatial grid for collision detection with optimal cell size
        from settings import SCREEN_WIDTH, SCREEN_HEIGHT

        self.spatial_grid = SpatialGrid(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            cell_size=50,  # Smaller cell size for better collision performance
        )

        # Performance tracking
        self.last_fps = 0
        self.last_update_time_ms = 0
        self.last_draw_time_ms = 0
        self.frame_count = 0

        # Memory management
        self.cleanup_interval = 2.0  # More frequent cleanup (seconds)
        self.last_cleanup_time = time.time()
        self.last_memory_optimization = time.time()

        # Debug flags
        self.debug_mode = False
        self.show_collision_grid = False

    def _init_object_pools(self):
        """Initialize object pools for efficient reuse"""
        from food import Food

        # Food object pool
        def create_food():
            return Food()

        def reset_food(food, *args, **kwargs):
            food.__init__(*args, **kwargs)

        self.food_pool = ObjectPool(
            create_food, reset_food, initial_size=30, max_size=100
        )

        # Particle effect pool (for environmental effects)
        def create_particle():
            return {
                "x": 0,
                "y": 0,
                "vx": 0,
                "vy": 0,
                "color": (255, 255, 255),
                "size": 1,
                "age": 0,
                "lifetime": 1.0,
                "active": False,
            }

        def reset_particle(particle, x=0, y=0, **kwargs):
            particle["x"] = x
            particle["y"] = y
            particle["vx"] = kwargs.get("vx", 0)
            particle["vy"] = kwargs.get("vy", 0)
            particle["color"] = kwargs.get("color", (255, 255, 255))
            particle["size"] = kwargs.get("size", 1)
            particle["age"] = 0
            particle["lifetime"] = kwargs.get("lifetime", 1.0)
            particle["active"] = True

        self.particle_pool = ObjectPool(
            create_particle, reset_particle, initial_size=200, max_size=1000
        )

    def start_frame(self):
        """Start frame timing and reset per-frame resources"""
        self.performance_monitor.start_frame()
        self.spatial_grid.clear()
        self.frame_count += 1

        # Perform periodic memory optimizations
        self._check_for_memory_optimization()

    def mark_update_complete(self):
        """Mark update phase complete and track performance"""
        self.performance_monitor.mark_update_time()
        self.last_update_time_ms = self.get_performance_stats().get("update_time_ms", 0)

    def mark_draw_complete(self):
        """Mark draw phase complete and track performance"""
        self.performance_monitor.mark_draw_time()
        self.last_draw_time_ms = self.get_performance_stats().get("draw_time_ms", 0)

        # Update FPS tracking
        stats = self.get_performance_stats()
        self.last_fps = stats.get("fps", 0)

        # Log performance data periodically
        if self.frame_count % 300 == 0:  # Every ~5 seconds at 60 FPS
            self._log_performance_data()

    def get_cached_text(self, text_str, size=14, color=(255, 255, 255)):
        """Get a cached Text object for efficient rendering"""
        return self.text_cache.get_text(text_str, size, color)

    def get_particle_from_pool(self, x=0, y=0, **kwargs):
        """Get a particle object from the pool with initial properties"""
        return self.particle_pool.get_object(x, y, **kwargs)

    def return_particle_to_pool(self, particle):
        """Return a particle object to the pool when done"""
        self.particle_pool.return_object(particle)

    def get_food_from_pool(self):
        """Get a food object from the pool"""
        return self.food_pool.get_object()

    def return_food_to_pool(self, food):
        """Return a food object to the pool"""
        self.food_pool.return_object(food)

    def update_spatial_grid(self, snakes, food_items):
        """Update spatial grid with current objects"""
        self.spatial_grid.clear()

        # Add snakes to grid
        for snake in snakes:
            if not snake.is_dead:
                self.spatial_grid.add_object(
                    snake, snake.head_position.x, snake.head_position.y
                )

        # Add food to grid
        for food in food_items:
            self.spatial_grid.add_object(food, food.position.x, food.position.y)

    def get_nearby_objects(self, x, y, radius=50):
        """Get objects near position using spatial grid"""
        return self.spatial_grid.get_nearby_objects(x, y, radius)

    def should_cleanup(self):
        """Check if cleanup should be performed"""
        current_time = time.time()
        if current_time - self.last_cleanup_time > self.cleanup_interval:
            self.last_cleanup_time = current_time
            return True
        return False

    def _check_for_memory_optimization(self):
        """Periodically perform memory optimization tasks"""
        current_time = time.time()

        # Every 10 seconds, perform thorough memory optimization
        # More frequent optimization (every 5 seconds) to prevent memory buildup
        if current_time - self.last_memory_optimization > 5.0:
            # Clear old text cache entries
            # More aggressive cache clearing
            if len(self.text_cache.cached_texts) > 30:
                # Clear 2/3 of the cache instead of half
                keys_to_remove = list(self.text_cache.cached_texts.keys())[::3]
                keys_to_remove += list(self.text_cache.cached_texts.keys())[1::3]
                for key in keys_to_remove:
                    del self.text_cache.cached_texts[key]
                self.text_cache.last_cleanup = current_time

            # Run garbage collection if memory usage seems high
            # or if the frame rate has dropped below 30 FPS
            # Lower threshold to catch performance issues earlier
            if self.last_fps < 45:
                gc.collect()

            # Record that we've done memory optimization
            self.last_memory_optimization = current_time

    def _log_performance_data(self):
        """Log performance statistics to help with optimization"""
        stats = self.get_performance_stats()
        text_cache_stats = self.text_cache.get_cache_stats()
        food_pool_stats = self.food_pool.get_performance_stats()
        particle_pool_stats = self.particle_pool.get_performance_stats()

        # Only print if in debug mode
        if self.debug_mode:
            print(f"--- Performance Stats ---")
            print(f"FPS: {stats['fps']:.1f}")
            print(f"Update time: {stats['update_time_ms']:.2f}ms")
            print(f"Draw time: {stats['draw_time_ms']:.2f}ms")
            print(
                f"Text cache: {text_cache_stats['cache_size']} items, "
                f"{text_cache_stats['hit_rate']:.1f}% hit rate"
            )
            print(
                f"Food pool: {food_pool_stats['active']} active, "
                f"{food_pool_stats['available']} available, "
                f"{food_pool_stats['reuse_rate']:.1f}% reuse rate"
            )
            print(
                f"Particle pool: {particle_pool_stats['active']} active, "
                f"{particle_pool_stats['available']} available"
            )
            print("-------------------------")

    def _log_performance_data(self):
        """Log performance statistics to help with optimization"""
        stats = self.get_performance_stats()
        text_cache_stats = self.text_cache.get_cache_stats()
        food_pool_stats = self.food_pool.get_performance_stats()
        particle_pool_stats = self.particle_pool.get_performance_stats()

        # Only print if in debug mode
        if self.debug_mode:
            print(f"--- Performance Stats ---")
            print(f"FPS: {stats['fps']:.1f}")
            print(f"Update time: {stats['update_time_ms']:.2f}ms")
            print(f"Draw time: {stats['draw_time_ms']:.2f}ms")
            print(
                f"Text cache: {text_cache_stats['cache_size']} items, "
                f"{text_cache_stats['hit_rate']:.1f}% hit rate"
            )
            print(
                f"Food pool: {food_pool_stats['active']} active, "
                f"{food_pool_stats['available']} available, "
                f"{food_pool_stats['reuse_rate']:.1f}% reuse rate"
            )
            print(
                f"Particle pool: {particle_pool_stats['active']} active, "
                f"{particle_pool_stats['available']} available"
            )
            print("-------------------------")

    def get_performance_stats(self):
        """Get current performance statistics"""
        stats = self.performance_monitor.get_stats()
        stats["active_food"] = len(self.food_pool.active_objects)
        stats["pooled_food"] = len(self.food_pool.available_objects)
        stats["active_particles"] = len(self.particle_pool.active_objects)
        stats["text_cache_size"] = len(self.text_cache.cached_texts)
        return stats
