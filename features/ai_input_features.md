# Advanced AI Input Features

## Overview

This document defines the comprehensive input feature set that AI agents receive to navigate the complex survival environment created by all advanced systems working together.

## Core Feature Categories

### 1. Basic Survival Features (Enhanced)

```python
basic_features = [
    # Self state (core)
    position_x, position_y,
    size_current, health_percentage, energy_percentage,
    movement_speed, direction_current,
    current_direction_vector_x, current_direction_vector_y,

    # Original core movement features
    food_distance_nearest, food_direction_x, food_direction_y,
    wall_distance_up, wall_distance_right, wall_distance_down, wall_distance_left,
    self_collision_risk_distance, self_collision_direction,
    hunter_proximity_distance, hunter_direction_x, hunter_direction_y,
    size_comparison_vs_nearest_threat, size_comparison_vs_nearest_prey,

    # Snake type and status
    is_hunter_status, is_normal_snake_status,
    starvation_time_remaining, starvation_warning_active,
    evolution_progress_to_hunter, hunter_transformation_ready,

    # Environment awareness
    food_items_visible_count, threat_entities_nearby_count,
    safe_zones_accessible, danger_level_current_area,
    nearest_safe_zone_distance, escape_routes_available,

    # Game state
    game_time_elapsed, entities_remaining,
    map_bounds_distance, center_distance,
    total_snakes_alive, hunters_vs_normal_ratio
]
```

### 1a. Special Food Effects Features

```python
special_food_features = [
    # Active effects status
    speed_boost_active, speed_boost_time_remaining,
    slow_effect_active, slow_effect_time_remaining,
    immunity_active, immunity_time_remaining,
    shrink_vulnerability, growth_opportunity_nearby,

    # Special food availability
    speed_food_nearby_distance, slow_food_nearby_distance,
    immunity_food_nearby_distance, growth_food_nearby_distance,
    shrink_food_nearby_distance, special_food_total_count,

    # Effect strategic value
    speed_boost_escape_value, immunity_hunting_value,
    growth_food_size_advantage, effect_combination_opportunities
]
```

### 1b. Environmental Effects Features

```python
environmental_features = [
    # Black holes
    black_holes_active_count, nearest_black_hole_distance,
    black_hole_pull_strength_current, black_hole_escape_difficulty,
    black_hole_threat_level, time_until_black_hole_spawn,

    # Speed zones
    speed_zones_active_count, nearest_speed_zone_distance,
    current_zone_speed_multiplier, zone_exit_distance,
    fast_zone_advantage_available, slow_zone_trap_risk,

    # Food magnets
    food_magnets_active_count, nearest_food_magnet_distance,
    food_magnet_pull_affecting_resources, magnet_competition_level,
    food_clustering_due_to_magnets, magnet_strategic_positioning
]
```

### 1c. Special Creatures Features

```python
creature_features = [
    # Ripper entities
    rippers_active_count, nearest_ripper_distance,
    ripper_target_status, ripper_threat_level_to_self,
    ripper_population_pressure, time_since_ripper_spawn,

    # Scavenger entities
    scavengers_active_count, nearest_scavenger_distance,
    scavenger_food_competition_level, food_theft_risk,
    scavenger_territory_overlap, resource_scarcity_due_to_scavengers,

    # Creature ecosystem balance
    creature_population_balance, ecosystem_stability,
    predator_prey_ratios, creature_spawn_predictions
]
```

### 2. Health System Features

```python
health_features = [
    current_hp_percentage,
    time_since_last_damage,
    damage_rate_current_location,
    nearest_healing_source_distance,
    healing_food_available_count,
    estimated_time_to_death_current_damage_rate,
    safe_zone_distance_for_healing,
    lingering_damage_effects_active,
    health_regeneration_rate_current_location
]
```

### 3. Energy Management Features

```python
energy_features = [
    current_energy_percentage,
    energy_state_enum,  # energized/normal/tired/exhausted
    time_since_last_rest,
    energy_consumption_rate_current_activity,
    sprint_capability_available,
    sprint_cooldown_remaining,
    energy_food_nearby_count,
    territory_energy_bonus_available,
    estimated_energy_for_planned_route
]
```

### 4. Poison Zone Features

```python
poison_features = [
    poison_zones_in_range_count,
    nearest_poison_zone_distance,
    poison_zone_movement_vectors,
    wind_direction_current,
    wind_strength_current,
    predicted_poison_zone_positions_5s,
    safe_path_to_goal_exists,
    poison_effect_remaining_duration,
    poison_damage_rate_current_location
]
```

### 5. Territory System Features

```python
territory_features = [
    owned_territories_count,
    territory_types_owned,
    nearest_claimable_territory_distance,
    territory_contest_status,
    territorial_defense_strength,
    territory_benefits_active,
    competitor_territorial_threats,
    territory_value_assessment_nearby,
    territorial_expansion_opportunities
]
```

### 6. Disaster System Features

```python
disaster_features = [
    current_disaster_active,
    disaster_type_current,
    disaster_time_remaining,
    time_until_next_disaster_estimate,
    nearest_shelter_distance,
    shelter_capacity_available,
    disaster_damage_rate_current_location,
    warning_level_current,
    evacuation_routes_available
]
```

### 7. Aerial Predator Features

```python
aerial_features = [
    sky_hunters_in_detection_range,
    nearest_sky_hunter_distance,
    sky_hunter_state_current,  # patrolling/hunting/diving
    aerial_threat_level,
    nearest_aerial_cover_distance,
    group_aerial_defense_active,
    aerial_vulnerability_level_current,
    sky_hunter_attack_imminent,
    aerial_escape_routes_count
]
```

### 8. Alliance System Features

```python
alliance_features = [
    current_alliance_status,
    alliance_member_count,
    alliance_type_current,
    alliance_trust_level,
    betrayal_risk_assessment,
    potential_alliance_partners_nearby,
    alliance_coordination_bonus_active,
    shared_resources_available,
    alliance_member_relative_positions,
    reputation_level_current
]
```

### 9. Advanced Spatial Intelligence

```python
spatial_features = [
    # Multi-layer threat assessment
    immediate_danger_level,
    medium_term_risk_5s,
    long_term_risk_15s,

    # Strategic positioning
    strategic_value_current_position,
    escape_routes_available_count,
    chokepoint_control_status,
    high_ground_advantage,

    # Movement optimization
    optimal_path_exists_to_goal,
    path_length_to_nearest_safety,
    movement_efficiency_current_route,
    terrain_advantage_factors
]
```

### 10. Resource Intelligence

```python
resource_features = [
    # Resource distribution
    food_density_local_area,
    resource_competition_level,
    resource_regeneration_rate_nearby,

    # Strategic resource control
    resource_monopoly_opportunities,
    resource_sharing_alliance_benefits,
    resource_hoarding_viability,

    # Long-term resource planning
    resource_sustainability_assessment,
    seasonal_resource_pattern_recognition,
    resource_scarcity_prediction
]
```

## Feature Engineering Pipeline

### Raw Sensor Data Processing

```python
class AdvancedFeatureExtractor:
    def __init__(self, game_state):
        self.game_state = game_state
        self.feature_history = deque(maxlen=100)  # Historical context
        self.pattern_recognizer = PatternRecognizer()

    def extract_all_features(self, entity):
        features = {}

        # Basic features
        features.update(self._extract_basic_features(entity))

        # System-specific features
        features.update(self._extract_health_features(entity))
        features.update(self._extract_energy_features(entity))
        features.update(self._extract_poison_features(entity))
        features.update(self._extract_territory_features(entity))
        features.update(self._extract_disaster_features(entity))
        features.update(self._extract_aerial_features(entity))
        features.update(self._extract_alliance_features(entity))

        # Advanced computed features
        features.update(self._extract_spatial_intelligence(entity))
        features.update(self._extract_resource_intelligence(entity))
        features.update(self._extract_temporal_patterns(entity))

        # Normalize and encode features
        return self._normalize_and_encode(features)

    def _extract_temporal_patterns(self, entity):
        """Extract time-based patterns and predictions"""
        return {
            "cyclical_threat_pattern": self._detect_threat_cycles(),
            "resource_availability_trend": self._analyze_resource_trends(),
            "optimal_action_timing": self._calculate_action_timing(),
            "survival_probability_short_term": self._predict_survival_5s(entity),
            "survival_probability_medium_term": self._predict_survival_30s(entity)
        }
```

### Contextual Feature Adaptation

```python
class ContextualFeatureWeighting:
    def __init__(self):
        self.context_weights = {
            "early_game": {"growth": 0.8, "safety": 0.2},
            "mid_game": {"growth": 0.5, "territory": 0.3, "safety": 0.2},
            "late_game": {"survival": 0.6, "territory": 0.4},
            "disaster_active": {"safety": 0.9, "other": 0.1},
            "alliance_active": {"cooperation": 0.4, "individual": 0.6}
        }

    def weight_features(self, features, context):
        weighted_features = features.copy()
        weights = self.context_weights.get(context, {})

        for feature_category, weight in weights.items():
            category_features = self._get_category_features(features, feature_category)
            for feature_name in category_features:
                weighted_features[feature_name] *= weight

        return weighted_features
```

## Feature Complexity Analysis

### Decision Complexity Metrics (Updated)

- **Feature Count**: 195+ individual input features (includes all original + new systems)
- **Feature Interactions**: 3,800+ potential pairwise interactions
- **Temporal Dependencies**: 35+ time-dependent feature relationships
- **Multi-System Integration**: 15 major system interaction matrices (original + advanced)
- **Strategic Depth**: 7+ levels of strategic planning required

### Information Processing Requirements (Updated)

```python
feature_processing_stats = {
    "raw_inputs_per_frame": 195,
    "derived_features_per_frame": 95,
    "historical_context_features": 40,
    "prediction_features": 30,
    "total_feature_vector_size": 360,

    "processing_frequency": "60 FPS",
    "feature_update_latency": "<16ms",
    "memory_requirements": "~75MB per agent",
    "computational_complexity": "O(n²) for n entities"
}
```

## AI Learning Challenges

### Multi-Objective Optimization

- **Competing Goals**: Survival vs growth vs territory vs alliances
- **Dynamic Priorities**: Context-dependent goal weighting
- **Risk Assessment**: Multi-dimensional risk/reward evaluation
- **Time Horizon**: Short-term vs long-term decision optimization

### Pattern Recognition Requirements

- **Spatial Patterns**: Terrain advantage recognition
- **Temporal Patterns**: Cyclical threat and resource patterns
- **Social Patterns**: Alliance formation and betrayal patterns
- **Causal Patterns**: Action-consequence relationship learning

### Adaptive Intelligence

- **Context Switching**: Rapid adaptation to changing game states
- **Strategy Evolution**: Learning new strategies as game complexity increases
- **Meta-Learning**: Learning to learn from limited experience
- **Transfer Learning**: Applying knowledge across different scenarios

## Benchmarking Metrics

### Survival Performance

```python
survival_metrics = {
    "basic_survival_time": "minutes survived",
    "adjusted_survival_score": "survival_time * complexity_multiplier",
    "threat_evasion_efficiency": "successful_threat_avoidances / total_threats",
    "resource_acquisition_rate": "resources_per_minute",
    "territorial_control_score": "territory_value * control_duration",
    "alliance_success_rate": "successful_alliances / attempted_alliances",
    "adaptation_speed": "time_to_optimal_strategy_in_new_environment"
}
```

### Strategic Sophistication

```python
sophistication_metrics = {
    "decision_tree_depth": "average_planning_horizon",
    "multi_objective_balance": "goal_achievement_across_categories",
    "emergent_behavior_complexity": "novel_strategy_generation_rate",
    "social_intelligence_score": "alliance_and_reputation_management",
    "environmental_mastery": "disaster_and_threat_survival_rate"
}
```

## Implementation Notes

### Feature Scaling and Normalization

- **Range Normalization**: All features scaled to [0, 1] or [-1, 1] ranges
- **Temporal Smoothing**: Moving averages for noisy environmental features
- **Categorical Encoding**: One-hot encoding for discrete state features
- **Missing Value Handling**: Default values for unavailable features

### Real-Time Processing Optimizations

- **Feature Caching**: Cache expensive-to-compute derived features
- **Incremental Updates**: Update only changed features per frame
- **Priority Processing**: Compute critical features first
- **Parallel Computation**: Multi-threaded feature extraction for multiple agents

### Memory Management

- **Feature History**: Limited sliding window of historical features
- **Compression**: Compact encoding for similar feature patterns
- **Garbage Collection**: Automatic cleanup of unused feature data
- **Memory Pooling**: Reuse feature vector allocations

This comprehensive feature set creates an unprecedented level of environmental complexity that will push AI agents to develop sophisticated survival intelligence rivaling human strategic thinking capabilities.

## Comprehensive Feature Summary

### Complete Feature Inventory

| Feature Category                  | Feature Count | Key Components                                     |
| --------------------------------- | ------------- | -------------------------------------------------- |
| **Basic Survival (Enhanced)**     | 25 features   | Core movement, snake status, environment awareness |
| **Special Food Effects**          | 16 features   | Active effects, food availability, strategic value |
| **Environmental Effects**         | 18 features   | Black holes, speed zones, food magnets             |
| **Special Creatures**             | 16 features   | Rippers, scavengers, ecosystem balance             |
| **Health System**                 | 9 features    | HP management, damage sources, healing             |
| **Energy Management**             | 9 features    | Stamina, sprint mechanics, energy efficiency       |
| **Poison Zones**                  | 9 features    | Moving hazards, wind patterns, damage prediction   |
| **Territory System**              | 9 features    | Ownership, control, territorial warfare            |
| **Disaster Events**               | 9 features    | Environmental catastrophes, shelter systems        |
| **Aerial Predators**              | 9 features    | Sky hunters, anti-air mechanics, group defense     |
| **Alliance System**               | 10 features   | Cooperation, trust, betrayal, reputation           |
| **Advanced Spatial Intelligence** | 12 features   | Multi-layer threat assessment, positioning         |
| **Resource Intelligence**         | 9 features    | Resource distribution, competition, sustainability |
| **Temporal Patterns**             | 10 features   | Predictive intelligence, timing optimization       |
| **Meta-Learning Features**        | 8 features    | Adaptation, strategy evolution, transfer learning  |

### **Total Feature Count: 195+ Individual Features**

### Original vs New Feature Systems Integration

#### Core Game Features (Already Implemented)

- **Movement & Navigation**: Wall distances, self-collision, directional control
- **Food System**: Regular food plus 5 special food types with complex effects
- **Snake Evolution**: Normal → Hunter transformation with size-based advantages
- **Environmental Hazards**: Black holes, speed zones, food magnets
- **Special Creatures**: Rippers (hunter population control), Scavengers (resource competition)
- **Starvation Mechanics**: Time-based survival pressure

#### Advanced Survival Features (To Be Implemented)

- **Health & Energy Systems**: Multi-resource management complexity
- **Poison Zones**: Dynamic moving environmental threats
- **Territory Control**: Strategic area ownership and conflicts
- **Disaster Events**: Large-scale environmental catastrophes
- **Aerial Predators**: Three-dimensional threat awareness
- **Alliance System**: Social cooperation and betrayal mechanics
