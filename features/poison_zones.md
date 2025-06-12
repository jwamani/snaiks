# Poison Zones System

## Overview

The Poison Zones System introduces dynamic environmental hazards that drift across the map, creating moving danger areas that force constant spatial awareness and adaptive pathfinding strategies for AI agents.

## Core Mechanics

### Poison Zone Properties

- **Appearance**: Purple-green swirling toxic clouds with warning borders
- **Size**: Variable radius (30-80 pixels) depending on toxicity level
- **Movement**: Slow drift following wind patterns (1-3 pixels/second)
- **Lifespan**: 45-90 seconds before dissipating naturally
- **Spawn Rate**: 1-3 zones active simultaneously, new zone every 20-40 seconds

### Damage System

- **Immediate Damage**: 1 HP per second while inside zone
- **Lingering Poison**: 0.5 HP per second for 3 seconds after leaving
- **Toxicity Levels**: Light (0.5 HP/sec), Medium (1.0 HP/sec), Heavy (1.5 HP/sec)
- **Immunity**: Brief 0.2-second immunity between damage ticks
- **Death Risk**: 10 seconds exposure = potential death

### Wind Pattern System

```python
class WindSystem:
    def __init__(self):
        self.wind_direction = random.uniform(0, 360)  # degrees
        self.wind_strength = random.uniform(0.5, 2.0)  # pixels/second
        self.wind_change_frequency = 15.0  # seconds
        self.last_wind_change = time.time()

    def update_wind(self):
        current_time = time.time()
        if current_time - self.last_wind_change > self.wind_change_frequency:
            # Gradual wind direction changes
            direction_change = random.uniform(-30, 30)
            self.wind_direction = (self.wind_direction + direction_change) % 360

            # Wind strength fluctuations
            strength_change = random.uniform(-0.3, 0.3)
            self.wind_strength = max(0.2, min(3.0, self.wind_strength + strength_change))

            self.last_wind_change = current_time

    def get_wind_vector(self):
        angle_rad = math.radians(self.wind_direction)
        return Vector2(
            math.cos(angle_rad) * self.wind_strength,
            math.sin(angle_rad) * self.wind_strength
        )
```

## Implementation Details

### Poison Zone Class

```python
class PoisonZone:
    def __init__(self, x, y, toxicity_level="medium"):
        self.position = Vector2(x, y)
        self.toxicity_level = toxicity_level
        self.radius = self._get_radius_for_toxicity(toxicity_level)
        self.damage_rate = self._get_damage_rate(toxicity_level)
        self.birth_time = time.time()
        self.lifespan = random.uniform(45, 90)
        self.entities_inside = set()
        self.wind_resistance = random.uniform(0.7, 1.3)

        # Visual properties
        self.swirl_angle = 0
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.particles = []

    def update(self, wind_vector, dt):
        # Move with wind (with some resistance)
        movement = wind_vector * self.wind_resistance * dt
        self.position += movement

        # Keep within screen bounds (with wrapping or bouncing)
        self._handle_boundary_collision()

        # Update visual effects
        self.swirl_angle += dt * 2.0  # Rotation speed
        self.pulse_phase += dt * 3.0  # Pulse speed
        self._update_particles(dt)

        # Check for entity collisions
        self._check_entity_collisions()

        # Apply damage to entities inside
        self._apply_poison_damage(dt)

    def _get_damage_rate(self, toxicity):
        rates = {"light": 0.5, "medium": 1.0, "heavy": 1.5}
        return rates.get(toxicity, 1.0)

    def _get_radius_for_toxicity(self, toxicity):
        radii = {"light": 30, "medium": 50, "heavy": 80}
        return radii.get(toxicity, 50)

    def is_inside(self, entity_position):
        distance = self.position.distance_to(entity_position)
        return distance <= self.radius

    def is_expired(self):
        return time.time() - self.birth_time > self.lifespan

    def draw(self, screen):
        # Draw swirling poison cloud with animated effects
        self._draw_poison_cloud(screen)
        self._draw_warning_border(screen)
        self._draw_particles(screen)
```

### Poison Effect Component

```python
class PoisonEffect:
    def __init__(self, entity, duration=3.0, damage_rate=0.5):
        self.entity = entity
        self.duration = duration
        self.damage_rate = damage_rate
        self.remaining_time = duration
        self.last_damage_time = time.time()

    def update(self, dt):
        self.remaining_time -= dt

        # Apply lingering poison damage
        current_time = time.time()
        if current_time - self.last_damage_time >= 1.0:  # Damage every second
            self.entity.health.take_damage(self.damage_rate, "lingering_poison")
            self.last_damage_time = current_time

    def is_expired(self):
        return self.remaining_time <= 0

    def draw_visual_effect(self, screen):
        # Draw green/purple poison aura around affected entity
        pass
```

## Strategic Impact

### Pathfinding Challenges

- Static pathfinding algorithms become ineffective
- Dynamic route planning required for safe travel
- Prediction of zone movement becomes valuable skill
- Emergency route changes when zones block paths

### Area Denial

- Poison zones temporarily claim territory
- Safe zones become more valuable during poison presence
- Chokepoints can be blocked by drifting zones
- Territory control affected by poison positioning

### Risk vs Reward

- Valuable resources may be in/near poison zones
- Risk assessment required for zone proximity
- Timing decisions for crossing contaminated areas
- Emergency evacuation planning from owned territories

## AI Learning Challenges

### Spatial Intelligence

- **Zone Tracking**: Monitor multiple moving hazard locations
- **Movement Prediction**: Anticipate zone drift patterns based on wind
- **Safe Path Planning**: Calculate routes avoiding current and future danger
- **Emergency Navigation**: Rapid route recalculation when paths are blocked

### Risk Assessment

- **Exposure Calculation**: Estimate damage from zone proximity/traversal
- **Health vs Goal Trade-offs**: Decide when poison exposure is worthwhile
- **Lingering Effect Planning**: Account for post-exposure poison damage
- **Group Coordination**: Navigate poison as alliance without losing members

### New Input Features

```python
poison_features = [
    nearest_poison_zone_distance,
    poison_zone_movement_vector,
    predicted_zone_position_5s,
    current_poison_effect_remaining,
    safe_path_to_goal_exists,
    wind_direction_current,
    poison_zones_blocking_territory,
    estimated_damage_to_traverse_zone,
    time_until_zone_expiration
]
```

### Emergent Behaviors

- **Wind Pattern Learning**: Recognize and predict wind direction changes
- **Poison Avoidance**: Sophisticated pathing around moving hazards
- **Timing Strategies**: Wait for zones to pass vs finding alternate routes
- **Risk-Benefit Analysis**: Calculate when poison exposure is worthwhile
- **Emergency Protocols**: Rapid evacuation when zones threaten critical areas

## Visual Design

### Poison Cloud Appearance

- **Core**: Dense purple-green swirling center
- **Edge**: Gradually fading toxic vapors
- **Animation**: Continuous rotation and pulsing
- **Particles**: Floating toxic droplets around perimeter
- **Warning Border**: Bright yellow/orange danger outline

### Wind Indicators

- **Wind Arrows**: Small directional indicators at map edges
- **Particle Trails**: Ambient particles showing wind direction
- **Zone Drift**: Visual trails showing recent zone movement
- **Prediction Lines**: Faint lines showing estimated zone paths

### Poison Effects on Entities

- **Damage Flash**: Red flash when taking poison damage
- **Lingering Aura**: Green/purple glow for poisoned entities
- **Health Indicator**: Poison damage shown in health bar
- **Movement Impairment**: Slightly slower movement when poisoned

## Integration Points

### With Health System

- Direct HP damage creates immediate survival pressure
- Lingering effects require health management
- Healing becomes critical after poison exposure

### With Territory System

- Poison zones can temporarily claim territories
- Territorial defense complicated by poison presence
- Safe territories gain value during poison events

### With Energy System

- Avoiding poison may require energy-expensive detours
- Sprint capability crucial for poison zone escapes
- Energy planning must account for poison avoidance

### With Disaster System

- Poison zones may intensify during certain disasters
- Shelter areas provide poison protection
- Compound threats when disasters and poison combine

## Configuration Options

```python
# Poison zone settings
ENABLE_POISON_ZONES = True
MAX_POISON_ZONES = 3
POISON_SPAWN_INTERVAL = (20, 40)  # seconds
POISON_ZONE_LIFESPAN = (45, 90)  # seconds
POISON_DAMAGE_RATES = {"light": 0.5, "medium": 1.0, "heavy": 1.5}
LINGERING_POISON_DURATION = 3.0
WIND_CHANGE_FREQUENCY = 15.0
WIND_STRENGTH_RANGE = (0.5, 2.0)
POISON_IMMUNITY_DURATION = 0.2
```

## Testing Scenarios

### Basic Poison Exposure

1. Snake enters poison zone
2. Takes 1 HP/second damage while inside
3. Exits zone and suffers 3 seconds lingering poison
4. Total damage: zone time + 1.5 HP from lingering effect

### Zone Movement Prediction

1. AI observes poison zone drift direction
2. Calculates wind pattern from movement
3. Predicts future zone position
4. Plans path avoiding predicted location

### Emergency Evacuation

1. Poison zone drifts toward snake's territory
2. Snake recognizes threat to owned area
3. Evacuates territory before zone arrival
4. Returns after zone passes or expires

### Multi-Zone Navigation

1. Multiple poison zones create maze-like environment
2. AI must find safe path through moving hazards
3. Dynamic re-routing as zones shift position
4. Risk assessment for zone proximity traversal

The Poison Zones System creates a dynamic, ever-changing threat landscape that prevents static strategies and forces AI agents to develop real-time adaptive intelligence for survival in a hostile environment.
