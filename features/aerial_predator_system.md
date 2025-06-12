# Aerial Predator System

## Overview

The Aerial Predator System introduces Sky Hunters - flying predators that patrol from above, creating a new dimension of threat that requires constant vigilance and anti-air awareness strategies.

## Core Mechanics

### Sky Hunter Properties

- **Appearance**: Large bird-like creatures with dark silhouettes and glowing red eyes
- **Movement**: Circular patrol patterns at high altitude, swooping attacks
- **Detection Range**: 150-pixel radius for spotting ground targets
- **Attack Pattern**: 3-second dive attack dealing 3 HP damage
- **Vulnerability Window**: 2 seconds on ground after attack before returning to air
- **Spawn Rate**: 1-2 Sky Hunters active simultaneously, respawn every 60-90 seconds

### Hunt Behavior System

```python
class SkyHunter:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.altitude = 200  # High altitude for patrolling
        self.state = "patrolling"  # patrolling, hunting, diving, recovering
        self.target = None
        self.patrol_center = Vector2(x, y)
        self.patrol_radius = 100
        self.detection_range = 150
        self.dive_speed = 300  # pixels/second
        self.attack_damage = 3
        self.vulnerability_duration = 2.0

    def update(self, dt, ground_entities):
        if self.state == "patrolling":
            self._patrol_behavior(dt)
            self._scan_for_targets(ground_entities)
        elif self.state == "hunting":
            self._track_target(dt)
        elif self.state == "diving":
            self._execute_dive_attack(dt)
        elif self.state == "recovering":
            self._recovery_behavior(dt)

    def _scan_for_targets(self, entities):
        for entity in entities:
            distance = self.position.distance_to(entity.position)
            if distance <= self.detection_range:
                # Prioritize larger, more isolated targets
                target_priority = entity.size * 0.7
                if not entity.is_in_shelter():
                    target_priority *= 1.5
                if not entity.has_nearby_allies(50):
                    target_priority *= 1.3

                if target_priority > 15:  # Minimum threshold for attack
                    self.target = entity
                    self.state = "hunting"
                    break

    def _execute_dive_attack(self, dt):
        if self.target:
            # Fast dive toward target
            direction = (self.target.position - self.position).normalize()
            self.position += direction * self.dive_speed * dt
            self.altitude = max(0, self.altitude - 400 * dt)  # Descend rapidly

            # Check for attack contact
            if self.position.distance_to(self.target.position) < 20:
                self._perform_attack()

    def _perform_attack(self):
        if self.target and self.target.health:
            self.target.health.take_damage(self.attack_damage, "aerial_attack")
            self.state = "recovering"
            self.altitude = 0  # On ground, vulnerable

        # Visual effects for attack
        self._create_dive_attack_effects()

    def is_vulnerable(self):
        return self.state == "recovering" and self.altitude <= 10
```

### Counter-Attack Mechanics

- **Ground Vulnerability**: Sky Hunters can be attacked when on ground after dive
- **Projectile Defense**: Certain items/abilities can hit flying hunters
- **Shelter Protection**: Covered areas provide complete aerial protection
- **Group Defense**: Multiple entities can coordinate anti-air defense

## Strategic Impact

### Constant Vigilance

- Open areas become dangerous due to aerial threat
- Shelter and cover gain significantly increased value
- Movement patterns must account for sky threat
- Large entities become priority targets for aerial attacks

### Defensive Positioning

- Covered areas and overhangs provide aerial protection
- Group movement provides mutual anti-air defense
- Timing of open-area crossings becomes critical
- Underground areas gain strategic value

### Size vs Safety Trade-off

- Larger entities more likely to be targeted by aerial predators
- Growth strategy must balance size advantage vs aerial vulnerability
- Medium-sized entities may have optimal risk/reward ratio
- Camouflage and stealth become viable strategies

## AI Learning Challenges

### Aerial Threat Assessment

- **Sky Scanning**: Constantly monitor aerial threats while navigating
- **Vulnerability Timing**: Recognize when aerial predators are hunting vs patrolling
- **Cover Utilization**: Efficiently use terrain features for aerial protection
- **Attack Pattern Recognition**: Learn Sky Hunter behavior patterns for prediction

### Anti-Air Strategy

- **Vulnerability Exploitation**: Identify and capitalize on Sky Hunter ground vulnerability
- **Cooperative Defense**: Coordinate with other entities for group anti-air protection
- **Evasion Tactics**: Develop effective escape patterns during aerial pursuit
- **Risk Assessment**: Balance open-area benefits vs aerial attack risk

### New Input Features

```python
aerial_features = [
    sky_hunters_in_detection_range,
    nearest_sky_hunter_distance,
    sky_hunter_state_current,  # patrolling/hunting/diving
    time_since_last_aerial_attack,
    nearest_aerial_cover_distance,
    group_anti_air_defense_strength,
    aerial_vulnerability_level,
    sky_hunter_target_priority_self,
    aerial_escape_routes_available
]
```

### Emergent Behaviors

- **Cover Hopping**: Moving between covered areas to avoid aerial detection
- **Aerial Awareness**: Maintaining constant vigilance for sky threats
- **Size Optimization**: Balancing growth vs aerial vulnerability
- **Group Coordination**: Forming defensive groups for aerial protection
- **Timing Strategy**: Coordinating actions with Sky Hunter patrol patterns

## Anti-Air Defense System

### Shelter Types for Aerial Protection

```python
aerial_shelter_types = {
    "cave_overhang": {
        "protection_level": "complete",
        "capacity": 3,
        "visibility": "hidden"
    },
    "tree_canopy": {
        "protection_level": "partial",
        "capacity": 2,
        "visibility": "camouflaged"
    },
    "building_roof": {
        "protection_level": "complete",
        "capacity": 5,
        "visibility": "obvious"
    },
    "underground_tunnel": {
        "protection_level": "complete",
        "capacity": 4,
        "visibility": "hidden"
    }
}
```

### Group Defense Mechanics

```python
class GroupAerialDefense:
    def __init__(self):
        self.defense_range = 60  # pixels
        self.minimum_group_size = 3
        self.defense_effectiveness = 0.8  # 80% chance to deter attack

    def calculate_group_defense(self, entities):
        groups = self._identify_defensive_groups(entities)
        for group in groups:
            if len(group) >= self.minimum_group_size:
                self._apply_aerial_defense_bonus(group)

    def _apply_aerial_defense_bonus(self, group):
        for entity in group:
            entity.aerial_defense_bonus = self.defense_effectiveness
            entity.group_defense_active = True
```

### Vulnerability Windows

- **Sky Hunter Recovery**: 2-second window when Sky Hunter is on ground
- **Dive Attack Pattern**: Predictable approach pattern during dive
- **Patrol Timing**: Regular patrol patterns create safe movement windows
- **Weather Interference**: Storms and disasters ground Sky Hunters temporarily

## Visual Design

### Sky Hunter Appearance

- **Silhouette**: Large, menacing bird-like shadow against sky
- **Eyes**: Glowing red scanning lights during hunting mode
- **Dive Effect**: Speed lines and shadow growing larger during attack
- **Vulnerability**: Visible landing and recovery animation on ground

### Aerial Threat Indicators

- **Detection Range**: Subtle circle showing Sky Hunter detection area
- **Threat Level**: UI indicator showing current aerial threat status
- **Cover Zones**: Highlighted areas providing aerial protection
- **Attack Warning**: Visual/audio warning when Sky Hunter begins dive

### Defense Visualization

- **Group Defense**: Visual links between entities providing mutual protection
- **Cover Status**: Clear indication when entity is protected from aerial attack
- **Vulnerability Display**: Warning indicators when in high aerial danger zones
- **Escape Routes**: Temporary pathfinding lines to nearest aerial cover

## Integration Points

### With Shelter System

- Aerial cover becomes additional shelter requirement
- Multi-threat shelter design (disasters + aerial + ground threats)
- Shelter value calculation includes aerial protection factor

### With Territory System

- Aerial-protected territories gain significant strategic value
- Underground territories become highly desirable
- Territory defense requires anti-air considerations

### With Alliance System

- Group aerial defense creates alliance formation incentives
- Coordinated anti-air strategies for alliance groups
- Mutual protection pacts specifically for aerial threats

### With Health System

- Aerial attacks cause significant health damage (3 HP)
- Health management must account for aerial attack possibility
- Healing locations require aerial protection consideration

## Configuration Options

```python
# Aerial predator settings
ENABLE_AERIAL_PREDATORS = True
MAX_SKY_HUNTERS = 2
SKY_HUNTER_SPAWN_INTERVAL = (60, 90)  # seconds
SKY_HUNTER_DETECTION_RANGE = 150
SKY_HUNTER_ATTACK_DAMAGE = 3
SKY_HUNTER_DIVE_SPEED = 300
VULNERABILITY_DURATION = 2.0
GROUP_DEFENSE_THRESHOLD = 3
AERIAL_DEFENSE_EFFECTIVENESS = 0.8
PATROL_ALTITUDE = 200
```

## Testing Scenarios

### Basic Aerial Attack

1. Sky Hunter detects large snake in open area
2. Enters hunting mode and begins pursuit
3. Executes dive attack dealing 3 HP damage
4. Vulnerable on ground for 2 seconds before returning to air

### Aerial Evasion

1. Snake spots incoming Sky Hunter in hunting mode
2. Rapidly moves to nearest overhead cover
3. Sky Hunter loses target and returns to patrol mode
4. Snake waits safely until threat passes

### Group Aerial Defense

1. Three snakes form defensive group in open area
2. Sky Hunter approaches but detects group defense
3. 80% chance attack is deterred by group coordination
4. Sky Hunter returns to patrol without attacking

### Vulnerability Exploitation

1. Sky Hunter attacks and lands on ground during recovery
2. Nearby snake recognizes vulnerability window
3. Counter-attacks Sky Hunter during 2-second ground phase
4. Sky Hunter takes damage and retreats with reduced health

The Aerial Predator System adds a three-dimensional threat element that forces AI agents to develop spatial awareness, timing strategies, and group coordination skills while balancing risk assessment for open-area activities.
