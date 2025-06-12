# Disaster Events System

## Overview

The Disaster Events System introduces large-scale environmental catastrophes that affect the entire game world, creating urgent survival scenarios that test AI adaptability and emergency response capabilities.

## Core Mechanics

### Disaster Types

#### Acid Rain Storm

- **Duration**: 20-30 seconds
- **Effect**: 2 HP/second damage to all entities not in shelter
- **Visual**: Green rain particles, toxic puddles forming
- **Warning**: 5-second warning with darkening sky
- **Shelter Requirements**: Enclosed areas, caves, buildings

#### Extreme Heat Wave

- **Duration**: 25-40 seconds
- **Effect**: 1.5 HP/second damage, energy drain 2x faster
- **Visual**: Heat shimmer effects, orange-red overlay
- **Warning**: Temperature gauge rising over 8 seconds
- **Protection**: Shade areas, underground shelters, water proximity

#### Volcanic Eruption

- **Duration**: 45-60 seconds
- **Effect**: Random lava projectiles (5 HP damage), ash reduces visibility
- **Visual**: Lava fountains, ash clouds, flying molten rocks
- **Warning**: Ground tremors and rumbling sounds for 10 seconds
- **Safe Zones**: Far from eruption center, underground areas

#### Toxic Gas Cloud

- **Duration**: 30-45 seconds
- **Effect**: 1 HP/second + lingering poison effect (double duration)
- **Visual**: Yellow-green gas spreading across map
- **Warning**: Wind change warnings, distant gas visibility
- **Protection**: High altitude areas, sealed shelters, gas masks (rare items)

#### Lightning Storm

- **Duration**: 15-25 seconds
- **Effect**: Random lightning strikes (8 HP damage), electromagnetic disruption
- **Visual**: Dark clouds, frequent lightning, electrical effects
- **Warning**: Static electricity buildup, distant thunder
- **Safety**: Low areas, avoid metal objects, underground shelter

### Disaster Scheduling System

```python
class DisasterManager:
    def __init__(self):
        self.disaster_queue = []
        self.active_disaster = None
        self.last_disaster_time = 0
        self.disaster_frequency = (120, 300)  # 2-5 minutes between disasters
        self.warning_time = 8.0  # seconds of warning before disaster
        self.disaster_types = [
            "acid_rain", "heat_wave", "volcanic_eruption",
            "toxic_gas", "lightning_storm"
        ]

    def schedule_next_disaster(self):
        next_disaster_time = random.uniform(*self.disaster_frequency)
        disaster_type = random.choice(self.disaster_types)

        self.disaster_queue.append({
            "type": disaster_type,
            "trigger_time": time.time() + next_disaster_time,
            "warning_issued": False
        })

    def update(self, dt):
        current_time = time.time()

        # Check for disaster warnings
        for disaster in self.disaster_queue:
            if not disaster["warning_issued"]:
                if current_time >= disaster["trigger_time"] - self.warning_time:
                    self._issue_disaster_warning(disaster)
                    disaster["warning_issued"] = True

        # Trigger disasters
        for disaster in self.disaster_queue:
            if current_time >= disaster["trigger_time"]:
                self._start_disaster(disaster)
                self.disaster_queue.remove(disaster)
                break

        # Update active disaster
        if self.active_disaster:
            self.active_disaster.update(dt)
            if self.active_disaster.is_finished():
                self.active_disaster = None
                self.last_disaster_time = current_time
```

## Strategic Impact

### Emergency Response

- Immediate survival becomes top priority during disasters
- Long-term planning interrupted by urgent survival needs
- Shelter seeking becomes critical survival skill
- Resource gathering must account for disaster timing

### Shelter Economics

- Shelter areas become extremely valuable during disasters
- Competition for limited shelter space during emergencies
- Shelter construction/claiming becomes strategic investment
- Temporary alliances form for mutual shelter sharing

### Predictive Planning

- Weather pattern recognition for disaster prediction
- Resource stockpiling before predicted disasters
- Strategic positioning near shelter areas
- Emergency evacuation route planning

## AI Learning Challenges

### Emergency Response

- **Disaster Recognition**: Identify disaster type from early warning signs
- **Shelter Prioritization**: Rapidly assess and move to nearest safe area
- **Resource Abandonment**: Know when to abandon current goals for survival
- **Panic Management**: Maintain strategic thinking during crisis situations

### Disaster Preparation

- **Pattern Recognition**: Learn disaster timing patterns and frequencies
- **Shelter Investment**: Invest in shelter access for long-term survival
- **Resource Timing**: Coordinate resource gathering with disaster schedules
- **Emergency Protocols**: Develop rapid response plans for each disaster type

### New Input Features

```python
disaster_features = [
    current_disaster_active,
    disaster_type_enum,
    time_until_next_disaster,
    nearest_shelter_distance,
    shelter_capacity_available,
    disaster_damage_rate_current_location,
    warning_level_current,
    time_remaining_in_disaster,
    safe_zone_locations_available
]
```

### Emergent Behaviors

- **Disaster Prediction**: Learning to recognize pre-disaster environmental cues
- **Emergency Evacuation**: Rapid, efficient movement to safety during warnings
- **Shelter Competition**: Strategic positioning for disaster shelter access
- **Recovery Planning**: Post-disaster resource and territory recovery strategies
- **Disaster Opportunism**: Using disasters to gain advantages over competitors

## Shelter System

### Shelter Types

```python
class Shelter:
    def __init__(self, shelter_type, position, capacity):
        self.type = shelter_type
        self.position = position
        self.capacity = capacity
        self.occupants = []
        self.protection_types = self._get_protection_types()
        self.entry_requirements = self._get_entry_requirements()

    def _get_protection_types(self):
        protections = {
            "cave": ["acid_rain", "toxic_gas", "heat_wave", "lightning"],
            "building": ["acid_rain", "lightning", "volcanic"],
            "underground": ["all_disasters"],
            "water_shelter": ["heat_wave", "lightning"],
            "elevated_shelter": ["toxic_gas", "volcanic"]
        }
        return protections.get(self.type, [])

    def can_protect_from(self, disaster_type):
        return (disaster_type in self.protection_types or
                "all_disasters" in self.protection_types)

    def has_capacity(self):
        return len(self.occupants) < self.capacity

    def attempt_entry(self, entity):
        if self.has_capacity():
            self.occupants.append(entity)
            entity.current_shelter = self
            return True
        return False
```

### Shelter Competition

- **Capacity Limits**: Shelters can only protect limited number of entities
- **First Come, First Served**: Early disaster response gets shelter priority
- **Size-Based Exclusion**: Larger entities may take multiple shelter spaces
- **Territorial Shelter Control**: Territory owners get priority shelter access

## Visual Design

### Disaster Warning Systems

- **Weather Indicators**: Barometric pressure, wind speed, temperature displays
- **Visual Warnings**: Sky color changes, cloud formations, atmospheric effects
- **Warning UI**: Countdown timers, danger level indicators
- **Environmental Cues**: Animal behavior, plant reactions, ground tremors

### Disaster Effects

- **Particle Systems**: Rain, ash, gas clouds, lightning effects
- **Environmental Changes**: Temporary terrain modifications, visibility reduction
- **Damage Visualization**: Flash effects when entities take disaster damage
- **Shelter Highlighting**: Clear visual indicators of safe areas during disasters

### Emergency UI

- **Shelter Finder**: Directional indicators to nearest available shelter
- **Disaster Timer**: Time remaining in current disaster event
- **Protection Status**: Clear indication of current protection level
- **Emergency Actions**: Rapid access to disaster-specific survival actions

## Integration Points

### With Health System

- Disasters are primary source of rapid health loss
- Shelter access becomes life-or-death decision
- Health preparation before disasters becomes strategic

### With Territory System

- Territorial shelters provide exclusive disaster protection
- Territory value dramatically increases during disasters
- Shelter territories become highly contested

### With Alliance System

- Shelter sharing creates temporary alliance incentives
- Cooperative disaster response improves survival rates
- Alliance shelters provide mutual protection

### With Energy System

- Emergency evacuation requires energy reserves
- Shelter seeking may require sprint capabilities
- Energy management critical for disaster preparation

## Configuration Options

```python
# Disaster system settings
ENABLE_DISASTERS = True
DISASTER_FREQUENCY = (120, 300)  # seconds between disasters
WARNING_TIME = 8.0  # seconds of warning before disaster
DISASTER_TYPES_ENABLED = [
    "acid_rain", "heat_wave", "volcanic_eruption",
    "toxic_gas", "lightning_storm"
]
SHELTER_CAPACITY_MULTIPLIER = 1.0
DISASTER_DAMAGE_RATES = {
    "acid_rain": 2.0,
    "heat_wave": 1.5,
    "volcanic_projectile": 5.0,
    "toxic_gas": 1.0,
    "lightning_strike": 8.0
}
```

## Testing Scenarios

### Basic Disaster Response

1. Heat wave warning issued (8-second countdown)
2. Snake identifies nearest shelter location
3. Rapidly moves to shelter before disaster starts
4. Survives 30-second heat wave in safety

### Shelter Competition

1. Acid rain warning during high entity density
2. Multiple snakes compete for limited shelter capacity
3. Larger/faster snakes secure shelter priority
4. Excluded entities take damage during disaster

### Disaster Pattern Learning

1. AI observes disaster timing patterns over multiple rounds
2. Learns to predict approximate disaster schedules
3. Positions near shelter areas before predicted disasters
4. Gains survival advantage through pattern recognition

### Emergency Alliance Formation

1. Volcanic eruption threatens multiple snakes
2. Temporary alliance forms for mutual shelter sharing
3. Cooperative evacuation to large shelter area
4. Alliance dissolves after disaster passes

The Disaster Events System creates high-stakes survival scenarios that interrupt long-term planning and force AI agents to develop emergency response capabilities while maintaining strategic thinking under extreme pressure.
