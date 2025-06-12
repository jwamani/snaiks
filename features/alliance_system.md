# Dynamic Alliance System

## Overview

The Dynamic Alliance System enables temporary and strategic cooperation between AI entities, creating complex social dynamics, betrayal mechanics, and group coordination challenges that significantly expand the strategic depth of survival scenarios.

## Core Mechanics

### Alliance Formation

- **Proximity-Based**: Entities can initiate alliances with nearby entities
- **Mutual Benefit**: Both parties must agree to alliance terms
- **Size Requirements**: Minimum similarity in size/capability for viable alliance
- **Duration**: Alliances last 30-120 seconds unless renewed or broken
- **Maximum Members**: 2-4 entities per alliance depending on total entity count

### Alliance Types

#### Survival Pact

- **Purpose**: Mutual protection during disasters and threats
- **Benefits**: Shared shelter access, coordinated threat response
- **Duration**: 60-90 seconds
- **Termination**: Automatic after disaster passes or by mutual agreement

#### Hunting Alliance

- **Purpose**: Coordinated resource gathering and territory control
- **Benefits**: Shared resource information, group hunting efficiency
- **Duration**: 45-60 seconds
- **Termination**: Resource scarcity or territorial conflicts

#### Defense Coalition

- **Purpose**: Mutual territorial defense and expansion
- **Benefits**: Combined defense strength, coordinated territorial expansion
- **Duration**: 90-120 seconds
- **Termination**: Territorial goals achieved or alliance member elimination

#### Emergency Alliance

- **Purpose**: Temporary cooperation during immediate crises
- **Benefits**: Rapid response coordination, resource sharing
- **Duration**: 30-45 seconds
- **Termination**: Crisis resolution or safer individual positioning

### Alliance Mechanics Implementation

```python
class Alliance:
    def __init__(self, initiator, target, alliance_type):
        self.members = [initiator, target]
        self.alliance_type = alliance_type
        self.formation_time = time.time()
        self.duration = self._get_alliance_duration(alliance_type)
        self.trust_level = 0.5  # 0.0 = hostile, 1.0 = complete trust
        self.shared_resources = []
        self.betrayal_risk = 0.1  # Base 10% chance of betrayal
        self.coordination_bonus = self._calculate_coordination_bonus()

    def _get_alliance_duration(self, alliance_type):
        durations = {
            "survival_pact": random.uniform(60, 90),
            "hunting_alliance": random.uniform(45, 60),
            "defense_coalition": random.uniform(90, 120),
            "emergency_alliance": random.uniform(30, 45)
        }
        return durations.get(alliance_type, 60)

    def add_member(self, new_member):
        if len(self.members) < 4 and self._is_compatible_member(new_member):
            self.members.append(new_member)
            self._recalculate_alliance_dynamics()
            return True
        return False

    def _calculate_betrayal_probability(self):
        # Factors that increase betrayal risk
        resource_scarcity = self._assess_resource_scarcity()
        size_imbalance = self._calculate_size_imbalance()
        territorial_overlap = self._assess_territorial_conflicts()

        self.betrayal_risk = (0.1 +
                            resource_scarcity * 0.3 +
                            size_imbalance * 0.2 +
                            territorial_overlap * 0.4)

        return min(0.8, self.betrayal_risk)  # Cap at 80% betrayal risk

    def execute_betrayal(self, betrayer, target):
        # Betrayal gives temporary advantage but destroys trust
        betrayer.size += target.size * 0.3  # Gain from betrayal
        target.health.take_damage(4, "betrayal_attack")

        # Remove betrayer from alliance
        self.members.remove(betrayer)
        betrayer.betrayal_history += 1
        betrayer.trust_reputation *= 0.5  # Reputation damage

        # Dissolve alliance if too few members
        if len(self.members) < 2:
            self.dissolve_alliance()
```

## Strategic Benefits

### Resource Efficiency

- **Information Sharing**: Alliance members share food and threat locations
- **Coordinated Harvesting**: Efficient resource gathering without competition
- **Resource Protection**: Mutual defense of valuable resource areas
- **Opportunity Coordination**: Synchronized actions for optimal resource acquisition

### Defensive Advantages

- **Mutual Protection**: Alliance members defend each other from threats
- **Combined Strength**: Group defense against larger individual threats
- **Threat Early Warning**: Shared threat detection and alert systems
- **Coordinated Retreat**: Organized evacuation during disasters or overwhelming threats

### Territorial Benefits

- **Expansion Coordination**: Synchronized territorial expansion strategies
- **Defense Sharing**: Mutual territorial defense and fortification
- **Territory Efficiency**: Complementary territory types for maximum benefit
- **Chokepoint Control**: Coordinated control of strategic map locations

## AI Learning Challenges

### Social Intelligence

- **Trust Assessment**: Evaluate reliability and betrayal risk of potential allies
- **Alliance Timing**: Recognize optimal moments for alliance formation/dissolution
- **Betrayal Detection**: Identify early warning signs of alliance member betrayal
- **Reputation Management**: Maintain trustworthy reputation for future alliance opportunities

### Coordination Strategy

- **Group Decision Making**: Participate in collective alliance strategy decisions
- **Resource Sharing**: Balance individual needs vs alliance benefit contributions
- **Tactical Coordination**: Execute synchronized actions with alliance members
- **Communication Protocols**: Develop effective signaling and coordination methods

### New Input Features

```python
alliance_features = [
    current_alliance_status,
    alliance_member_count,
    alliance_trust_level,
    betrayal_risk_assessment,
    alliance_coordination_bonus,
    potential_alliance_partners_nearby,
    alliance_duration_remaining,
    shared_resources_available,
    alliance_member_locations,
    alliance_threat_assessment
]
```

### Emergent Behaviors

- **Trust Building**: Gradual trust development through cooperative actions
- **Strategic Betrayal**: Calculated betrayal timing for maximum advantage
- **Alliance Networks**: Formation of complex multi-alliance relationships
- **Reputation Systems**: Long-term reputation tracking affecting alliance formation
- **Conditional Cooperation**: Context-dependent alliance behavior adaptation

## Trust and Betrayal Mechanics

### Trust Development

```python
class TrustSystem:
    def __init__(self):
        self.trust_factors = {
            "resource_sharing": 0.1,    # Trust gain per resource shared
            "threat_warning": 0.15,     # Trust gain for threat alerts
            "mutual_defense": 0.2,      # Trust gain for defensive actions
            "goal_achievement": 0.25    # Trust gain for alliance goal completion
        }

    def update_trust(self, alliance, action_type, actor, beneficiary):
        if action_type in self.trust_factors:
            trust_gain = self.trust_factors[action_type]
            alliance.trust_level = min(1.0, alliance.trust_level + trust_gain)

            # Individual trust between specific members
            actor.individual_trust[beneficiary] += trust_gain * 1.5

    def calculate_betrayal_temptation(self, entity, alliance):
        # Factors that make betrayal more tempting
        size_advantage_potential = self._calculate_betrayal_gains(entity, alliance)
        resource_desperation = entity._assess_resource_desperation()
        territorial_competition = self._assess_territorial_conflicts(entity, alliance)

        temptation = (size_advantage_potential * 0.4 +
                     resource_desperation * 0.3 +
                     territorial_competition * 0.3)

        return temptation
```

### Betrayal Consequences

- **Immediate Gains**: Betrayer gains 30% of betrayed entity's size
- **Reputation Damage**: Long-term trust reputation severely damaged
- **Alliance Dissolution**: Betrayal typically destroys the alliance
- **Future Alliance Difficulty**: Harder to form future alliances due to reputation
- **Retaliation Risk**: Other alliance members may seek revenge

### Betrayal Recovery

- **Reputation Rehabilitation**: Slow trust recovery through consistent cooperation
- **Redemption Actions**: Specific actions that restore reputation faster
- **Time-Based Forgiveness**: Gradual reputation recovery over time
- **Alliance Restrictions**: Limited alliance types available to known betrayers

## Visual Indicators

### Alliance Status

- **Member Linking**: Subtle visual connections between alliance members
- **Color Coordination**: Alliance members share similar color indicators
- **Trust Visualization**: Trust level shown through bond strength/color
- **Alliance Type**: Different visual styles for different alliance types

### Alliance Actions

- **Coordination Indicators**: Visual cues showing coordinated actions
- **Resource Sharing**: Animation effects for resource sharing between members
- **Mutual Defense**: Special effects when alliance members assist each other
- **Betrayal Flash**: Dramatic visual effect when betrayal occurs

### Trust and Reputation

- **Trust Meter**: Visual trust level indicator for active alliances
- **Reputation Indicator**: Entity reputation level for alliance formation
- **Betrayal History**: Visual markers for entities with betrayal history
- **Alliance Opportunity**: Indicators showing potential alliance formation chances

## Integration Points

### With Territory System

- **Shared Territories**: Alliance members can share territorial benefits
- **Coordinated Expansion**: Synchronized territorial conquest strategies
- **Defense Coordination**: Mutual territorial defense and reinforcement
- **Territory Trading**: Strategic territory exchanges between alliance members

### With Combat System

- **Group Combat**: Alliance members fight together against common threats
- **Coordinated Attacks**: Synchronized combat actions for maximum effectiveness
- **Defensive Support**: Alliance members provide combat assistance
- **Betrayal Combat**: Special combat mechanics during betrayal events

### With Resource System

- **Resource Pooling**: Alliance members share resources for mutual benefit
- **Information Sharing**: Shared knowledge of resource locations
- **Harvesting Coordination**: Efficient resource gathering without competition
- **Emergency Sharing**: Resource assistance during member crisis situations

### With Disaster System

- **Mutual Shelter**: Alliance members share disaster shelter access
- **Coordinated Evacuation**: Group evacuation strategies during disasters
- **Emergency Assistance**: Alliance support during disaster emergencies
- **Recovery Cooperation**: Post-disaster recovery assistance and coordination

## Configuration Options

```python
# Alliance system settings
ENABLE_ALLIANCE_SYSTEM = True
MAX_ALLIANCE_SIZE = 4
ALLIANCE_FORMATION_RANGE = 80  # pixels
TRUST_GAIN_RATE = 0.1
BETRAYAL_SIZE_GAIN = 0.3  # percentage of betrayed entity size
REPUTATION_DECAY_RATE = 0.05  # reputation recovery per minute
ALLIANCE_DURATION_RANGE = (30, 120)  # seconds
BASE_BETRAYAL_RISK = 0.1
MAX_BETRAYAL_RISK = 0.8
TRUST_THRESHOLD_FOR_ALLIANCE = 0.3
```

## Testing Scenarios

### Basic Alliance Formation

1. Two similar-sized snakes encounter resource scarcity
2. Proximity-based alliance formation triggers
3. Both entities agree to hunting alliance
4. Begin coordinated resource gathering with shared information

### Trust Development

1. Alliance members consistently share resources
2. Trust level gradually increases through cooperation
3. Members provide mutual defense during threat encounters
4. Strong trust bond develops, reducing betrayal risk

### Strategic Betrayal

1. Alliance member grows significantly larger than partner
2. Resource scarcity increases betrayal temptation
3. Larger member calculates optimal betrayal timing
4. Executes betrayal for size gain but suffers reputation damage

### Alliance Network Formation

1. Multiple small alliances form independently
2. Successful alliances attract additional members
3. Complex alliance network develops across map
4. Network coordination for large-scale territorial control

### Betrayal Recovery

1. Entity with betrayal history struggles to form new alliances
2. Demonstrates consistent cooperative behavior over time
3. Slowly rebuilds reputation through helpful actions
4. Eventually regains ability to form trusted alliances

The Dynamic Alliance System transforms SNAIKS from individual survival into complex social survival, requiring AI agents to develop sophisticated social intelligence, trust assessment, and group coordination capabilities that mirror real-world social dynamics.
