# Advanced Health System

## Overview

The Advanced Health System introduces HP-based survival mechanics, creating vulnerability and healing dynamics that add strategic depth to the survival simulation.

## Core Mechanics

### Health Points

- **Maximum HP**: 10 HP for all creatures
- **Starting HP**: All entities spawn at full health
- **Visual Indicator**: Health bar above entity heads when damaged
- **Death Condition**: Reaching 0 HP results in immediate death

### Damage Sources

| Source            | Damage Rate         | Notes                                |
| ----------------- | ------------------- | ------------------------------------ |
| Poison Zones      | 1 HP/second         | Continuous while inside zone         |
| Disaster Exposure | 2 HP/second         | During acid rain, heat waves         |
| Aerial Attacks    | 3 HP per hit        | Sky hunter swooping attacks          |
| Combat Damage     | 2 HP per engagement | Snake vs snake territorial conflicts |
| Lingering Poison  | 0.5 HP/second       | 3-second effect after leaving poison |

### Healing Mechanisms

| Method               | Healing Rate   | Requirements                        |
| -------------------- | -------------- | ----------------------------------- |
| Natural Regeneration | 0.1 HP/second  | In safe zones only                  |
| Shelter Rest         | 0.2 HP/second  | Inside shelter during disasters     |
| Healing Food         | +3 HP instant  | Special golden healing food items   |
| Territory Bonus      | 0.15 HP/second | In owned territory while stationary |

## Implementation Details

### Health Component

```python
class HealthComponent:
    def __init__(self, max_hp=10):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.damage_sources = []  # Track active damage effects
        self.healing_sources = []  # Track active healing effects
        self.last_damage_time = 0
        self.immunity_duration = 0  # Brief immunity after taking damage

    def take_damage(self, amount, source):
        if self.immunity_duration <= 0:
            self.current_hp = max(0, self.current_hp - amount)
            self.immunity_duration = 0.1  # 100ms damage immunity
            self.last_damage_time = time.time()
            return True
        return False

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def is_alive(self):
        return self.current_hp > 0

    def get_health_percentage(self):
        return self.current_hp / self.max_hp
```

### Visual Health Indicators

- **Health Bar**: Red/yellow/green bar above damaged entities
- **Damage Flash**: Brief red flash when taking damage
- **Healing Glow**: Soft green glow during healing
- **Critical Health**: Pulsing red outline when below 25% HP

## Strategic Impact

### Risk Assessment

- Snakes must evaluate damage vs benefit for risky areas
- Low health creates urgency for healing sources
- Health management becomes resource allocation decision

### Territorial Value

- Safe zones become highly contested
- Healing territories gain strategic importance
- Shelter locations become critical during disasters

### Combat Dynamics

- Multi-hit combat system for territorial disputes
- Health advantage in prolonged conflicts
- Retreat becomes viable tactical option

## AI Learning Challenges

### Health-Aware Decision Making

- **Damage Prediction**: Learn to assess environmental dangers
- **Healing Priority**: Recognize when to seek healing vs other goals
- **Risk Tolerance**: Adjust behavior based on current health level
- **Retreat Timing**: Know when to abandon objectives for safety

### New Input Features

```python
health_features = [
    current_hp_percentage,
    time_since_last_damage,
    nearest_healing_source_distance,
    damage_rate_in_current_area,
    estimated_time_to_death,
    safe_zone_distance,
    healing_food_availability
]
```

### Emergent Behaviors

- **Health Conservation**: Avoiding unnecessary risks when injured
- **Healing Prioritization**: Seeking healing sources over food when critical
- **Damage Trading**: Accepting minor damage for strategic advantages
- **Emergency Evacuation**: Rapid retreat patterns when health is critical

## Integration Points

### With Poison Zones

- Continuous damage creates urgency
- Lingering effects require strategic timing
- Safe path planning becomes essential

### With Disaster System

- Shelter seeking becomes life-or-death
- Health preparation before disasters
- Emergency healing during events

### With Territory System

- Healing territories become valuable assets
- Health advantage in territorial conflicts
- Recovery zones strategic positioning

### With Energy System

- Low health may reduce energy efficiency
- Healing may require energy investment
- Health/energy balance decisions

## Configuration Options

```python
# Health system settings
ENABLE_HEALTH_SYSTEM = True
MAX_HP = 10
DAMAGE_IMMUNITY_DURATION = 0.1
HEALING_FOOD_SPAWN_RATE = 0.05
NATURAL_REGEN_RATE = 0.1
SHELTER_HEALING_MULTIPLIER = 2.0
HEALTH_BAR_DISPLAY = True
```

## Testing Scenarios

### Basic Health Loss

1. Snake enters poison zone
2. Takes 1 HP/second damage
3. Health bar appears and decreases
4. Snake exits zone before death

### Healing Recovery

1. Damaged snake finds healing food
2. Instant +3 HP restoration
3. Health bar updates immediately
4. Visual healing effects display

### Combat Damage

1. Two snakes engage in territorial dispute
2. Both take 2 HP damage per engagement
3. Health advantages determine victor
4. Loser retreats to heal

This health system creates the foundation for all damage-based features while adding meaningful survival complexity that AI agents must learn to navigate effectively.
