# Territory System

## Overview

The Territory System introduces claimable areas that provide strategic advantages, creating complex ownership dynamics, resource competition, and territorial warfare that significantly elevate AI strategic thinking requirements.

## Core Mechanics

### Territory Types

#### Resource Territories

- **Food Spawning Zones**: 25% faster food generation within territory
- **Healing Sanctuaries**: 50% faster health regeneration while resting
- **Energy Wells**: 100% faster energy regeneration in designated areas
- **Size**: 100-150 pixel radius circular areas
- **Value**: High strategic worth, heavily contested

#### Shelter Territories

- **Disaster Protection**: Complete immunity to environmental disasters
- **Safe Zones**: Protection from aerial predators and certain creatures
- **Rest Bonuses**: Enhanced healing and energy regeneration
- **Capacity**: Limited occupancy (3-5 entities maximum)
- **Value**: Critical during disaster events

#### Strategic Territories

- **Chokepoints**: Control access to valuable areas of the map
- **Observation Posts**: Enhanced vision range and threat detection
- **Ambush Points**: Stealth bonuses and attack advantages
- **Escape Routes**: Quick access to safe areas during emergencies

### Territory Ownership Mechanics

```python
class Territory:
    def __init__(self, x, y, territory_type, size=100):
        self.center = Vector2(x, y)
        self.territory_type = territory_type
        self.radius = size
        self.owner = None
        self.ownership_strength = 0  # 0-100, stronger = harder to take
        self.contested = False
        self.challengers = []
        self.benefits = self._get_territory_benefits(territory_type)
        self.last_challenge_time = 0
        self.defense_bonus = 0

    def attempt_claim(self, entity):
        if self.owner is None:
            # Unclaimed territory - easy to claim
            if self._entity_in_territory(entity):
                self._start_claiming_process(entity)
        else:
            # Contested claim
            self._initiate_territorial_challenge(entity)

    def _start_claiming_process(self, entity):
        # Claiming takes time and presence
        claim_time = 10.0  # seconds to claim empty territory
        entity.territorial_action = {
            "type": "claiming",
            "territory": self,
            "time_remaining": claim_time,
            "start_time": time.time()
        }

    def _initiate_territorial_challenge(self, challenger):
        if challenger.size >= self.owner.size * 0.8:  # Must be reasonably sized
            self.contested = True
            self.challengers.append(challenger)
            self.last_challenge_time = time.time()

            # Challenge resolution methods
            self._resolve_territorial_dispute()

    def _resolve_territorial_dispute(self):
        # Size-based dominance
        total_challenger_size = sum(c.size for c in self.challengers)
        owner_size = self.owner.size if self.owner else 0

        # Energy investment factor
        challenger_energy = sum(c.energy.current_energy for c in self.challengers)
        owner_energy = self.owner.energy.current_energy if self.owner else 0

        # Calculate dominance score
        challenger_score = total_challenger_size * 0.7 + challenger_energy * 0.3
        owner_score = owner_size * 0.7 + owner_energy * 0.3 + self.defense_bonus

        if challenger_score > owner_score:
            self._transfer_ownership()
        else:
            self._repel_challengers()

    def _transfer_ownership(self):
        # Strongest challenger becomes new owner
        new_owner = max(self.challengers, key=lambda c: c.size)
        self.owner = new_owner
        self.ownership_strength = min(100, new_owner.size * 2)
        self.contested = False
        self.challengers.clear()

    def get_benefits_for_entity(self, entity):
        if entity == self.owner and self._entity_in_territory(entity):
            return self.benefits
        return {}
```

### Territorial Benefits

#### Resource Generation Bonuses

```python
territory_benefits = {
    "food_spawning": {
        "food_spawn_rate_multiplier": 1.25,
        "special_food_chance_bonus": 0.05,
        "description": "25% faster food spawning"
    },
    "healing_sanctuary": {
        "health_regen_multiplier": 1.5,
        "poison_resistance": 0.5,
        "description": "50% faster healing, poison resistance"
    },
    "energy_well": {
        "energy_regen_multiplier": 2.0,
        "sprint_cooldown_reduction": 0.5,
        "description": "Double energy regeneration"
    },
    "shelter": {
        "disaster_immunity": True,
        "aerial_predator_protection": True,
        "description": "Complete disaster and aerial protection"
    }
}
```

## Strategic Impact

### Resource Control

- Territories become strategic assets worth fighting for
- Long-term planning required for territorial expansion
- Resource territories provide compound advantages over time
- Territory loss significantly impacts survival capabilities

### Defensive Positioning

- Territorial ownership encourages defensive play styles
- Defense bonuses reward staying in owned territory
- Multiple territory ownership creates empire-building incentives
- Strategic territory placement controls map flow

### Conflict Generation

- Valuable territories naturally create conflict zones
- Size-based dominance encourages growth for territorial control
- Alliance formation for territorial conquest becomes viable
- Territorial disputes add complexity beyond simple survival

## AI Learning Challenges

### Strategic Planning

- **Territory Valuation**: Assess strategic worth of different territories
- **Expansion Strategy**: Plan territorial conquest based on current capabilities
- **Defense Prioritization**: Decide which territories to defend vs abandon
- **Investment Timing**: Know when to invest energy/health in territorial control

### Conflict Management

- **Challenge Assessment**: Evaluate chances of successful territorial challenge
- **Defense Allocation**: Balance resources between expansion and defense
- **Strategic Retreat**: Recognize when to abandon territories vs fight
- **Alliance Formation**: Coordinate with others for territorial conquest

### New Input Features

```python
territory_features = [
    owned_territories_count,
    nearest_unclaimed_territory_distance,
    territory_value_assessment,
    territorial_challenge_probability,
    defense_resources_available,
    competitor_territorial_strength,
    territory_benefits_active,
    contested_territory_resolution_time,
    alliance_territorial_support_available
]
```

### Emergent Behaviors

- **Empire Building**: Systematic territorial expansion strategies
- **Defensive Positioning**: Fortification and territory consolidation
- **Strategic Abandonment**: Calculated territory sacrifice for advantages
- **Territorial Warfare**: Complex multi-territory conflict management
- **Alliance Territories**: Cooperative territory control and sharing

## Territorial Warfare Mechanics

### Challenge System

```python
class TerritorialChallenge:
    def __init__(self, territory, challenger, owner):
        self.territory = territory
        self.challenger = challenger
        self.owner = owner
        self.challenge_type = self._determine_challenge_type()
        self.duration = self._get_challenge_duration()
        self.resolution_method = self._get_resolution_method()

    def _determine_challenge_type(self):
        size_ratio = self.challenger.size / self.owner.size
        if size_ratio >= 1.2:
            return "dominance"  # Size-based takeover
        elif size_ratio >= 0.8:
            return "contest"    # Energy-based competition
        else:
            return "harassment" # Harassment without takeover

    def resolve_challenge(self):
        if self.challenge_type == "dominance":
            return self._resolve_dominance_challenge()
        elif self.challenge_type == "contest":
            return self._resolve_contest_challenge()
        else:
            return self._resolve_harassment()

    def _resolve_contest_challenge(self):
        # Energy and persistence based
        challenger_commitment = self.challenger.energy.current_energy * 0.5
        owner_commitment = self.owner.energy.current_energy * 0.7  # Home advantage

        # Apply energy costs
        self.challenger.energy.consume_energy(challenger_commitment, "territorial_challenge")
        self.owner.energy.consume_energy(owner_commitment, "territorial_defense")

        return challenger_commitment > owner_commitment
```

### Territory Defense

- **Defense Bonuses**: Owners get combat advantages in their territory
- **Energy Efficiency**: Lower energy costs for actions in owned territory
- **Reinforcement**: Ability to call allied entities for territorial defense
- **Fortification**: Temporary defensive structures in high-value territories

## Visual Indicators

### Territory Boundaries

- **Ownership**: Color-coded borders indicating current owner
- **Contested**: Flashing/animated borders during challenges
- **Unclaimed**: Neutral gray dotted boundaries
- **Territory Type**: Different border patterns for territory types

### Ownership Status

- **Owner Indicator**: Small flag or symbol showing current owner
- **Ownership Strength**: Border thickness indicates ownership stability
- **Challenge Progress**: Visual progress indicators during disputes
- **Benefits Active**: Subtle visual effects showing active territory bonuses

### Territorial Actions

- **Claiming Animation**: Gradual border color change during claiming
- **Challenge Effects**: Combat-like visual effects during territorial disputes
- **Defense Mode**: Enhanced visual indicators when territory is under threat
- **Benefit Visualization**: Clear indicators of active territorial advantages

## Integration Points

### With Health System

- Healing territories provide medical advantages
- Territorial conflicts may involve health damage
- Territory control crucial for healing access during low health

### With Energy System

- Energy territories provide stamina advantages
- Territorial defense requires energy investment
- Energy efficiency bonuses in owned territories

### With Combat System

- Territories worth fighting for create natural conflict zones
- Territorial bonuses affect combat effectiveness
- Defense bonuses encourage territorial defensive strategies

### With Alliance System

- Cooperative territory control and sharing
- Allied territorial defense and expansion
- Territory-based alliance formation incentives

## Configuration Options

```python
# Territory system settings
ENABLE_TERRITORY_SYSTEM = True
MAX_TERRITORIES_PER_MAP = 8
TERRITORY_TYPES = ["food_spawning", "healing_sanctuary", "energy_well", "shelter"]
CLAIMING_TIME = 10.0  # seconds to claim empty territory
CHALLENGE_RESOLUTION_TIME = 5.0  # seconds to resolve territorial dispute
OWNERSHIP_DECAY_RATE = 0.1  # ownership strength loss per minute when absent
DEFENSE_BONUS_MULTIPLIER = 1.3
TERRITORY_SIZE_RANGE = (75, 150)  # pixel radius
```

## Testing Scenarios

### Territory Claiming

1. Snake discovers unclaimed food spawning territory
2. Begins 10-second claiming process while staying in area
3. Successfully claims territory and receives benefits
4. Territory border changes color to indicate ownership

### Territorial Challenge

1. Smaller snake challenges larger snake's territory
2. Challenge fails due to size disadvantage
3. Challenger takes energy damage from failed attempt
4. Owner's territorial strength increases from successful defense

### Strategic Territory War

1. Two large snakes compete for valuable healing sanctuary
2. Extended territorial conflict with multiple challenge attempts
3. Alliance members provide support during territorial defense
4. Territory changes hands multiple times during prolonged conflict

### Territory-Based Empire Building

1. Snake systematically claims multiple adjacent territories
2. Creates territorial empire with interconnected benefits
3. Develops defensive strategies for protecting territorial holdings
4. Uses territorial advantages to grow stronger and expand further

The Territory System transforms SNAIKS from simple survival into complex strategic territory control, requiring AI agents to develop sophisticated planning, conflict management, and empire-building capabilities that rival human strategic thinking.
