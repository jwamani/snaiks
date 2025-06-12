# Energy Management System

## Overview

The Energy Management System introduces stamina mechanics that govern movement, combat, and special abilities, creating resource allocation decisions that significantly impact AI strategy development.

## Core Mechanics

### Energy Pool

- **Maximum Energy**: 100 energy points for all creatures
- **Starting Energy**: All entities spawn at full energy
- **Visual Indicator**: Blue energy bar below health bar when not at maximum
- **Energy States**: Energized (80-100%), Normal (40-79%), Tired (20-39%), Exhausted (0-19%)

### Energy Consumption

| Activity          | Energy Cost             | Duration                   |
| ----------------- | ----------------------- | -------------------------- |
| Normal Movement   | 0.1/second              | Continuous                 |
| Sprint Movement   | 0.3/second              | 2x speed boost             |
| Combat Actions    | 2.0/action              | Per territorial engagement |
| Special Abilities | 5.0/use                 | Enhanced hunting, evasion  |
| Territory Defense | 1.0/second              | While actively defending   |
| Size Maintenance  | 0.05/second per segment | Larger snakes cost more    |

### Energy Regeneration

| Method          | Regeneration Rate | Requirements                     |
| --------------- | ----------------- | -------------------------------- |
| Stationary Rest | 0.15/second       | Not moving for 2+ seconds        |
| Territory Bonus | 0.25/second       | In owned territory while resting |
| Energy Food     | +20 instant       | Special blue energy food items   |
| Shelter Rest    | 0.3/second        | Inside shelter areas             |
| Pack Bonus      | 0.2/second        | Resting with alliance members    |

### Energy State Effects

#### Energized (80-100%)

- Full movement speed
- All abilities available
- Sprint capability enabled
- Enhanced combat effectiveness

#### Normal (40-79%)

- Standard movement speed
- Normal ability usage
- Reduced sprint duration
- Normal combat effectiveness

#### Tired (20-39%)

- 85% movement speed
- Ability cooldowns increased
- No sprint capability
- Reduced combat damage

#### Exhausted (0-19%)

- 60% movement speed
- Most abilities disabled
- Vulnerability to predators increased
- Combat effectiveness severely reduced

## Implementation Details

### Energy Component

```python
class EnergyComponent:
    def __init__(self, max_energy=100):
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.energy_state = "energized"
        self.sprint_mode = False
        self.last_activity_time = time.time()
        self.resting_duration = 0

    def consume_energy(self, amount, activity_type):
        if self.current_energy >= amount:
            self.current_energy = max(0, self.current_energy - amount)
            self.last_activity_time = time.time()
            self.resting_duration = 0
            return True
        return False

    def regenerate_energy(self, rate_multiplier=1.0):
        base_rate = 0.15  # Base regeneration rate
        regen_rate = base_rate * rate_multiplier
        self.current_energy = min(self.max_energy, self.current_energy + regen_rate)

    def update_energy_state(self):
        percentage = self.current_energy / self.max_energy
        if percentage >= 0.8:
            self.energy_state = "energized"
        elif percentage >= 0.4:
            self.energy_state = "normal"
        elif percentage >= 0.2:
            self.energy_state = "tired"
        else:
            self.energy_state = "exhausted"

    def can_sprint(self):
        return self.energy_state in ["energized", "normal"] and self.current_energy >= 10

    def get_speed_multiplier(self):
        multipliers = {
            "energized": 1.0,
            "normal": 1.0,
            "tired": 0.85,
            "exhausted": 0.6
        }
        return multipliers[self.energy_state]
```

### Sprint Mechanics

```python
class SprintSystem:
    def __init__(self):
        self.sprint_speed_multiplier = 2.0
        self.sprint_energy_cost = 0.3  # per second
        self.sprint_cooldown = 3.0  # seconds after exhaustion

    def can_activate_sprint(self, entity):
        return (entity.energy.can_sprint() and
                not entity.is_in_cooldown("sprint"))

    def activate_sprint(self, entity):
        entity.energy.sprint_mode = True
        entity.movement.speed_multiplier *= self.sprint_speed_multiplier
        entity.energy.consume_energy(self.sprint_energy_cost, "sprint")

    def deactivate_sprint(self, entity):
        entity.energy.sprint_mode = False
        entity.movement.speed_multiplier /= self.sprint_speed_multiplier
        if entity.energy.current_energy <= 0:
            entity.add_cooldown("sprint", self.sprint_cooldown)
```

## Strategic Impact

### Movement Strategy

- Energy becomes a limiting factor for exploration
- Sprint usage requires tactical timing
- Rest periods become strategically necessary
- Territory positioning affects energy efficiency

### Combat Dynamics

- Energy advantage determines fight outcomes
- Exhausted entities become vulnerable
- Energy management crucial for territorial defense
- Combat timing depends on energy reserves

### Resource Allocation

- Energy vs other resource trade-offs
- Investment in energy-efficient territories
- Sprint usage for emergency situations
- Long-term energy planning for survival

## AI Learning Challenges

### Energy-Aware Planning

- **Energy Budgeting**: Allocate energy across activities optimally
- **Rest Timing**: Know when to rest vs continue activity
- **Sprint Strategy**: Use speed boosts for maximum advantage
- **Energy Prediction**: Estimate energy costs for planned actions

### New Input Features

```python
energy_features = [
    current_energy_percentage,
    energy_state_enum,
    time_since_last_rest,
    energy_regen_rate_current_location,
    estimated_energy_for_planned_action,
    nearest_energy_food_distance,
    sprint_cooldown_remaining,
    territory_energy_bonus_available
]
```

### Emergent Behaviors

- **Energy Conservation**: Efficient movement patterns in low energy states
- **Strategic Resting**: Optimal rest timing and location selection
- **Sprint Optimization**: Tactical speed boost usage for escapes/hunts
- **Territory Energy**: Prioritizing energy-efficient territory control
- **Fatigue Management**: Avoiding exhaustion through proactive rest

## Integration Points

### With Health System

- Low energy may slow healing rates
- Energy required for emergency health actions
- Energy/health balance in survival decisions

### With Territory System

- Energy-efficient territories become valuable
- Energy costs for territorial defense
- Rest bonuses in owned territories

### With Combat System

- Energy determines combat effectiveness
- Exhaustion creates vulnerability windows
- Energy recovery between conflicts

### With Disaster System

- Energy reserves needed for disaster survival
- Sprint capability crucial for shelter reaching
- Energy management during long disasters

## Visual Indicators

### Energy Bar

- **Color**: Blue gradient from bright (full) to dark (empty)
- **Position**: Below health bar when visible
- **Animation**: Smooth depletion and regeneration
- **State Colors**: Different shades for energy states

### Energy State Effects

- **Energized**: Slight blue aura around entity
- **Tired**: Slower movement animation
- **Exhausted**: Panting animation, red fatigue indicators
- **Sprinting**: Speed lines and blue trail effects

### Energy Food

- **Appearance**: Bright blue pulsing orbs
- **Effect**: Lightning-like energy absorption animation
- **Spawn Rate**: Lower than normal food (5% of total spawns)
- **Value**: High priority target when energy is low

## Configuration Options

```python
# Energy system settings
ENABLE_ENERGY_SYSTEM = True
MAX_ENERGY = 100
BASE_MOVEMENT_COST = 0.1
SPRINT_SPEED_MULTIPLIER = 2.0
SPRINT_ENERGY_COST = 0.3
BASE_REGEN_RATE = 0.15
TERRITORY_REGEN_BONUS = 0.1
ENERGY_FOOD_SPAWN_RATE = 0.05
SIZE_ENERGY_MULTIPLIER = 0.05
```

## Testing Scenarios

### Energy Depletion

1. Snake moves continuously without rest
2. Energy gradually depletes over time
3. Movement speed reduces as energy drops
4. Snake forced to rest when exhausted

### Sprint Usage

1. Snake activates sprint mode
2. Speed doubles but energy drains quickly
3. Sprint deactivates when energy too low
4. Cooldown period before next sprint

### Territory Energy Bonus

1. Snake claims energy-efficient territory
2. Resting in territory provides bonus regeneration
3. Energy advantage enables more aggressive play
4. Territory becomes strategic asset

### Combat Energy Management

1. Two snakes engage in territorial combat
2. Higher energy snake has combat advantage
3. Exhausted snake becomes vulnerable
4. Energy recovery affects follow-up actions

The Energy Management System creates a resource allocation puzzle that AI agents must master to survive long-term, adding depth to every decision from movement to combat to territorial control.
