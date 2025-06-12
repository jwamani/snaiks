# Practical AI Implementation Example

## Overview

This document provides concrete code examples showing how to implement the advanced AI features in the SNAIKS game. We'll build the complete pipeline step by step.

---

## 1. Enhanced Feature Extractor Implementation

### 1.1 Core Feature Extractor Class

```python
import numpy as np
import time
from collections import deque
import math

class AdvancedFeatureExtractor:
    def __init__(self, game_state):
        self.game_state = game_state
        self.feature_cache = {}
        self.last_cache_update = 0
        self.cache_duration = 0.1  # Cache expensive features for 100ms

        # Feature categories for organization
        self.feature_categories = {
            'basic': [],
            'spatial': [],
            'temporal': [],
            'strategic': [],
            'environmental': [],
            'social': []
        }

    def extract_all_features(self, snake):
        """Main feature extraction function - returns complete feature vector"""
        current_time = time.time()
        features = {}

        # Always extract basic features (fast)
        features.update(self._extract_basic_features(snake))
        features.update(self._extract_spatial_features(snake))

        # Cache expensive features
        if current_time - self.last_cache_update > self.cache_duration:
            expensive_features = self._extract_expensive_features(snake)
            self.feature_cache.update(expensive_features)
            self.last_cache_update = current_time

        features.update(self.feature_cache)

        # Convert to normalized vector
        return self._features_to_vector(features)

    def _extract_basic_features(self, snake):
        """Extract core movement and status features"""
        features = {}

        # Positional features
        features['pos_x'] = snake.head.x / self.game_state.screen_width
        features['pos_y'] = snake.head.y / self.game_state.screen_height
        features['size'] = min(snake.size / 50.0, 1.0)  # Normalized size

        # Movement features
        features['speed'] = snake.speed / snake.max_speed
        features['dir_x'] = snake.direction.x
        features['dir_y'] = snake.direction.y

        # Status features
        features['is_hunter'] = 1.0 if snake.is_hunter else 0.0
        features['evolution_progress'] = snake.food_consumed / 10.0  # Progress to hunter

        # Survival pressure
        time_since_food = time.time() - snake.last_food_time
        features['starvation_urgency'] = min(time_since_food / 10.0, 1.0)
        features['time_to_death'] = max(0, (10.0 - time_since_food) / 10.0)

        return features

    def _extract_spatial_features(self, snake):
        """Extract spatial awareness features"""
        features = {}

        # Wall distances (critical for survival)
        features['wall_up'] = snake.head.y / self.game_state.screen_height
        features['wall_down'] = (self.game_state.screen_height - snake.head.y) / self.game_state.screen_height
        features['wall_left'] = snake.head.x / self.game_state.screen_width
        features['wall_right'] = (self.game_state.screen_width - snake.head.x) / self.game_state.screen_width

        # Food awareness
        food_data = self._analyze_food_situation(snake)
        features.update(food_data)

        # Threat assessment
        threat_data = self._analyze_threats(snake)
        features.update(threat_data)

        # Environmental hazards
        env_data = self._analyze_environment(snake)
        features.update(env_data)

        return features

    def _analyze_food_situation(self, snake):
        """Analyze food availability and strategic value"""
        features = {}

        # Find nearest food
        food_items = self.game_state.food_items
        if food_items:
            distances = [snake.head.distance_to(food.position) for food in food_items]
            nearest_idx = np.argmin(distances)
            nearest_food = food_items[nearest_idx]
            nearest_distance = distances[nearest_idx]

            # Distance and direction to nearest food
            features['food_distance'] = min(nearest_distance / 200.0, 1.0)
            direction = (nearest_food.position - snake.head).normalize()
            features['food_dir_x'] = direction.x
            features['food_dir_y'] = direction.y

            # Food type strategic assessment
            features['food_type_value'] = self._assess_food_value(nearest_food, snake)

            # Food density in area
            local_food_count = sum(1 for food in food_items
                                 if snake.head.distance_to(food.position) < 100)
            features['food_density'] = min(local_food_count / 5.0, 1.0)

        else:
            # No food available - critical situation
            features['food_distance'] = 1.0
            features['food_dir_x'] = 0.0
            features['food_dir_y'] = 0.0
            features['food_type_value'] = 0.0
            features['food_density'] = 0.0

        return features

    def _analyze_threats(self, snake):
        """Analyze threat situation for survival decisions"""
        features = {}

        # Find nearest hunter threat
        hunters = [s for s in self.game_state.snakes
                  if s.is_hunter and s != snake and s.is_alive]

        if hunters:
            distances = [snake.head.distance_to(hunter.head) for hunter in hunters]
            nearest_idx = np.argmin(distances)
            nearest_hunter = hunters[nearest_idx]
            nearest_distance = distances[nearest_idx]

            # Hunter proximity and threat level
            features['hunter_distance'] = min(nearest_distance / 300.0, 1.0)

            # Threat level based on size comparison
            size_ratio = snake.size / nearest_hunter.size
            features['threat_level'] = max(0, (1.2 - size_ratio))  # Threat when hunter bigger

            # Direction for avoidance
            direction = (nearest_hunter.head - snake.head).normalize()
            features['threat_dir_x'] = direction.x
            features['threat_dir_y'] = direction.y

        else:
            features['hunter_distance'] = 1.0
            features['threat_level'] = 0.0
            features['threat_dir_x'] = 0.0
            features['threat_dir_y'] = 0.0

        # Self-collision risk
        collision_risk = self._calculate_self_collision_risk(snake)
        features['self_collision_risk'] = collision_risk

        return features

    def _analyze_environment(self, snake):
        """Analyze environmental effects and hazards"""
        features = {}

        # Black hole analysis
        black_holes = [effect for effect in self.game_state.environmental_effects
                      if hasattr(effect, 'type') and effect.type == 'black_hole']

        if black_holes:
            nearest_hole = min(black_holes,
                             key=lambda h: snake.head.distance_to(h.position))
            distance = snake.head.distance_to(nearest_hole.position)

            features['black_hole_distance'] = min(distance / 150.0, 1.0)
            features['black_hole_pull'] = nearest_hole.calculate_pull_strength(snake.head)

            # Escape difficulty assessment
            escape_vector = (snake.head - nearest_hole.position).normalize()
            current_velocity = snake.direction
            escape_alignment = escape_vector.dot(current_velocity)
            features['black_hole_escape'] = (escape_alignment + 1.0) / 2.0  # 0-1 range

        else:
            features['black_hole_distance'] = 1.0
            features['black_hole_pull'] = 0.0
            features['black_hole_escape'] = 1.0

        # Speed zone analysis
        current_zone = self._get_current_speed_zone(snake)
        if current_zone:
            features['speed_multiplier'] = current_zone.speed_multiplier
            features['zone_exit_distance'] = self._distance_to_zone_edge(snake, current_zone) / 100.0
            features['zone_advantage'] = 1.0 if current_zone.speed_multiplier > 1.0 else 0.0
        else:
            features['speed_multiplier'] = 1.0
            features['zone_exit_distance'] = 1.0
            features['zone_advantage'] = 0.0

        return features

    def _extract_expensive_features(self, snake):
        """Extract computationally expensive features (cached)"""
        features = {}

        # Strategic positioning analysis
        features.update(self._analyze_strategic_position(snake))

        # Population dynamics
        features.update(self._analyze_population_dynamics(snake))

        # Advanced threat assessment
        features.update(self._analyze_complex_threats(snake))

        return features

    def _analyze_strategic_position(self, snake):
        """Analyze strategic value of current position"""
        features = {}

        # Map center proximity (safer generally)
        center = Vector2(self.game_state.screen_width / 2,
                        self.game_state.screen_height / 2)
        center_distance = snake.head.distance_to(center)
        features['center_distance'] = center_distance / 400.0  # Normalized

        # Border risk assessment
        min_wall_distance = min(
            snake.head.x, snake.head.y,
            self.game_state.screen_width - snake.head.x,
            self.game_state.screen_height - snake.head.y
        )
        features['border_risk'] = max(0, (50 - min_wall_distance) / 50.0)

        # Escape route analysis
        escape_routes = self._count_escape_routes(snake)
        features['escape_routes'] = min(escape_routes / 4.0, 1.0)

        return features

    def _analyze_population_dynamics(self, snake):
        """Analyze population pressure and competition"""
        features = {}

        total_snakes = len([s for s in self.game_state.snakes if s.is_alive])
        hunters = len([s for s in self.game_state.snakes if s.is_hunter and s.is_alive])

        # Population pressure
        features['population_pressure'] = min(total_snakes / 20.0, 1.0)
        features['hunter_ratio'] = hunters / max(total_snakes, 1)

        # Local competition
        nearby_snakes = sum(1 for s in self.game_state.snakes
                           if s != snake and s.is_alive and
                           snake.head.distance_to(s.head) < 150)
        features['local_competition'] = min(nearby_snakes / 5.0, 1.0)

        return features

    def _features_to_vector(self, features):
        """Convert feature dictionary to normalized numpy vector"""
        # Define feature order for consistent vectors
        feature_order = [
            'pos_x', 'pos_y', 'size', 'speed', 'dir_x', 'dir_y',
            'is_hunter', 'evolution_progress', 'starvation_urgency', 'time_to_death',
            'wall_up', 'wall_down', 'wall_left', 'wall_right',
            'food_distance', 'food_dir_x', 'food_dir_y', 'food_type_value', 'food_density',
            'hunter_distance', 'threat_level', 'threat_dir_x', 'threat_dir_y', 'self_collision_risk',
            'black_hole_distance', 'black_hole_pull', 'black_hole_escape',
            'speed_multiplier', 'zone_exit_distance', 'zone_advantage',
            'center_distance', 'border_risk', 'escape_routes',
            'population_pressure', 'hunter_ratio', 'local_competition'
        ]

        # Create vector with default values
        vector = []
        for feature_name in feature_order:
            value = features.get(feature_name, 0.0)
            # Ensure value is in valid range
            value = max(0.0, min(1.0, value))
            vector.append(value)

        return np.array(vector, dtype=np.float32)
```

---

## 2. Enhanced AI Agent Implementation

### 2.1 Advanced Snake AI Class

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import pickle
import os

class EnhancedSnakeAI:
    def __init__(self, snake_id, game_state):
        self.snake_id = snake_id
        self.game_state = game_state
        self.feature_extractor = AdvancedFeatureExtractor(game_state)

        # ML Model
        self.model = DecisionTreeClassifier(
            max_depth=20,
            min_samples_split=15,
            min_samples_leaf=8,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced action data
        )

        # Training data
        self.training_data = deque(maxlen=5000)  # Limit memory usage
        self.model_trained = False

        # Performance tracking
        self.decision_history = deque(maxlen=1000)
        self.performance_metrics = {
            'survival_time': 0,
            'food_efficiency': 0,
            'threat_avoidance': 0,
            'decisions_made': 0,
            'good_decisions': 0
        }

        # Exploration parameters
        self.exploration_rate = 0.15  # 15% random exploration
        self.exploration_decay = 0.995
        self.min_exploration = 0.05

        # Load existing model if available
        self._load_model()

    def decide_action(self, snake):
        """Main decision-making function"""
        # Extract features
        feature_vector = self.feature_extractor.extract_all_features(snake)

        # Get action from model or rules
        if self.model_trained:
            action = self._model_decision(feature_vector, snake)
        else:
            action = self._rule_based_decision(feature_vector, snake)

        # Record decision for training
        self._record_decision(feature_vector, action, snake)

        # Update exploration rate
        self.exploration_rate = max(self.min_exploration,
                                  self.exploration_rate * self.exploration_decay)

        return action

    def _model_decision(self, feature_vector, snake):
        """Use trained model to make decision"""
        try:
            # Get action probabilities
            action_probs = self.model.predict_proba([feature_vector])[0]

            # Apply exploration strategy
            if np.random.random() < self.exploration_rate:
                # Random exploration
                action_index = np.random.randint(0, 4)
            else:
                # Exploit learned strategy
                action_index = np.argmax(action_probs)

            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            return actions[action_index]

        except Exception as e:
            print(f"Model decision error: {e}")
            return self._rule_based_decision(feature_vector, snake)

    def _rule_based_decision(self, feature_vector, snake):
        """Fallback rule-based decision making"""
        # Convert vector back to feature names for easier logic
        features = self._vector_to_features(feature_vector)

        # Emergency rules - highest priority
        if features['self_collision_risk'] > 0.3:
            return self._avoid_self_collision(snake)

        if features['wall_up'] < 0.1 or features['wall_down'] < 0.1 or \
           features['wall_left'] < 0.1 or features['wall_right'] < 0.1:
            return self._avoid_walls(features)

        # Threat avoidance
        if features['threat_level'] > 0.5 and features['hunter_distance'] < 0.3:
            return self._flee_from_threat(features)

        # Opportunity pursuit
        if snake.is_hunter and features['threat_level'] < 0.2:
            prey_action = self._pursue_prey(snake, features)
            if prey_action:
                return prey_action

        # Food seeking (default behavior)
        return self._seek_food(features)

    def _record_decision(self, feature_vector, action, snake):
        """Record decision for later training"""
        # Calculate immediate reward
        reward = self._calculate_immediate_reward(snake, action)

        # Store training sample
        action_index = ['UP', 'DOWN', 'LEFT', 'RIGHT'].index(action)
        sample = {
            'features': feature_vector.copy(),
            'action': action_index,
            'reward': reward,
            'timestamp': time.time(),
            'snake_size': snake.size,
            'snake_position': (snake.head.x, snake.head.y)
        }

        self.training_data.append(sample)

        # Track decision quality
        self.performance_metrics['decisions_made'] += 1
        if reward > 0:
            self.performance_metrics['good_decisions'] += 1

        # Trigger training periodically
        if len(self.training_data) >= 500 and len(self.training_data) % 100 == 0:
            self._train_model()

    def _calculate_immediate_reward(self, snake, action):
        """Calculate reward signal for action quality"""
        reward = 0.0

        # Basic survival reward
        if snake.is_alive:
            reward += 0.1

        # Starvation urgency penalty
        features = self.feature_extractor._extract_basic_features(snake)
        if features['starvation_urgency'] > 0.8:
            reward -= 0.5

        # Food consumption reward
        if hasattr(snake, 'just_ate_food') and snake.just_ate_food:
            reward += 2.0

        # Size growth reward
        if hasattr(snake, 'size_last_frame'):
            size_gain = snake.size - snake.size_last_frame
            reward += size_gain * 0.5

        # Danger penalty
        spatial_features = self.feature_extractor._extract_spatial_features(snake)
        if spatial_features['threat_level'] > 0.7:
            reward -= 0.3

        return reward

    def _train_model(self):
        """Train the decision tree model"""
        if len(self.training_data) < 50:
            return

        try:
            # Prepare training data
            X = []
            y = []
            sample_weights = []

            for sample in self.training_data:
                X.append(sample['features'])
                y.append(sample['action'])
                # Weight recent samples more heavily
                age = time.time() - sample['timestamp']
                weight = np.exp(-age / 300)  # Exponential decay over 5 minutes
                weight *= max(0.1, sample['reward'] + 1)  # Reward-based weighting
                sample_weights.append(weight)

            X = np.array(X)
            y = np.array(y)
            sample_weights = np.array(sample_weights)

            # Train model
            self.model.fit(X, y, sample_weight=sample_weights)
            self.model_trained = True

            # Evaluate performance
            cv_scores = cross_val_score(self.model, X, y, cv=3)
            accuracy = np.mean(cv_scores)

            print(f"Snake {self.snake_id} - Model accuracy: {accuracy:.3f}, "
                  f"Training samples: {len(self.training_data)}")

            # Save model periodically
            if len(self.training_data) % 500 == 0:
                self._save_model()

        except Exception as e:
            print(f"Training error for snake {self.snake_id}: {e}")

    def _save_model(self):
        """Save trained model to disk"""
        try:
            model_data = {
                'model': self.model,
                'training_samples': len(self.training_data),
                'performance_metrics': self.performance_metrics,
                'exploration_rate': self.exploration_rate
            }

            filename = f"models/snake_ai_{self.snake_id}.pkl"
            os.makedirs("models", exist_ok=True)

            with open(filename, 'wb') as f:
                pickle.dump(model_data, f)

        except Exception as e:
            print(f"Model save error: {e}")

    def _load_model(self):
        """Load existing model from disk"""
        try:
            filename = f"models/snake_ai_{self.snake_id}.pkl"
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    model_data = pickle.load(f)

                self.model = model_data['model']
                self.performance_metrics = model_data.get('performance_metrics', self.performance_metrics)
                self.exploration_rate = model_data.get('exploration_rate', self.exploration_rate)
                self.model_trained = True

                print(f"Loaded model for snake {self.snake_id}")

        except Exception as e:
            print(f"Model load error: {e}")

    def get_performance_summary(self):
        """Get AI performance statistics"""
        if self.performance_metrics['decisions_made'] > 0:
            decision_quality = (self.performance_metrics['good_decisions'] /
                              self.performance_metrics['decisions_made'])
        else:
            decision_quality = 0.0

        return {
            'model_trained': self.model_trained,
            'training_samples': len(self.training_data),
            'decision_quality': decision_quality,
            'exploration_rate': self.exploration_rate,
            'survival_time': self.performance_metrics['survival_time']
        }
```

---

## 3. Integration with Game Loop

### 3.1 Game Manager Integration

```python
class GameManager:
    def __init__(self):
        # ... existing initialization ...
        self.snake_ais = {}  # AI agents for each snake
        self.ai_performance_tracker = AIPerformanceTracker()

    def create_snake(self, snake_id):
        """Create snake with AI agent"""
        snake = Snake(snake_id, self.get_random_position())

        # Create AI agent for this snake
        ai_agent = EnhancedSnakeAI(snake_id, self)
        self.snake_ais[snake_id] = ai_agent

        return snake

    def update_snakes(self, dt):
        """Update all snakes with AI decisions"""
        for snake in self.snakes:
            if snake.is_alive:
                # Get AI decision
                ai_agent = self.snake_ais.get(snake.id)
                if ai_agent:
                    action = ai_agent.decide_action(snake)
                    self._execute_snake_action(snake, action)

                # Update snake
                snake.update(dt)

                # Track performance
                self._update_ai_performance(snake, ai_agent)

    def _execute_snake_action(self, snake, action):
        """Execute AI decision on snake"""
        direction_map = {
            'UP': Vector2(0, -1),
            'DOWN': Vector2(0, 1),
            'LEFT': Vector2(-1, 0),
            'RIGHT': Vector2(1, 0)
        }

        new_direction = direction_map.get(action)
        if new_direction:
            # Prevent immediate self-collision
            if new_direction != -snake.direction:
                snake.direction = new_direction

    def _update_ai_performance(self, snake, ai_agent):
        """Track AI performance metrics"""
        if ai_agent:
            # Update survival time
            ai_agent.performance_metrics['survival_time'] = (
                time.time() - snake.birth_time
            )

            # Update food efficiency
            if snake.food_consumed > 0:
                ai_agent.performance_metrics['food_efficiency'] = (
                    snake.food_consumed / ai_agent.performance_metrics['survival_time']
                )

    def get_ai_statistics(self):
        """Get comprehensive AI performance statistics"""
        stats = {}
        for snake_id, ai_agent in self.snake_ais.items():
            stats[snake_id] = ai_agent.get_performance_summary()

        return stats
```

### 3.2 Performance Monitoring

```python
class AIPerformanceTracker:
    def __init__(self):
        self.session_data = []
        self.learning_curves = {
            'survival_time': [],
            'decision_quality': [],
            'exploration_rate': [],
            'model_accuracy': []
        }

    def record_session(self, snake_ais):
        """Record performance data from a game session"""
        session_stats = {
            'timestamp': time.time(),
            'snakes': {}
        }

        for snake_id, ai_agent in snake_ais.items():
            performance = ai_agent.get_performance_summary()
            session_stats['snakes'][snake_id] = performance

            # Update learning curves
            self.learning_curves['survival_time'].append(
                performance['survival_time']
            )
            self.learning_curves['decision_quality'].append(
                performance['decision_quality']
            )
            self.learning_curves['exploration_rate'].append(
                performance['exploration_rate']
            )

        self.session_data.append(session_stats)

    def generate_learning_report(self):
        """Generate comprehensive learning progress report"""
        if not self.session_data:
            return "No performance data available"

        recent_sessions = self.session_data[-10:]  # Last 10 sessions

        # Calculate averages
        avg_survival = np.mean([
            np.mean([snake['survival_time'] for snake in session['snakes'].values()])
            for session in recent_sessions
        ])

        avg_decision_quality = np.mean([
            np.mean([snake['decision_quality'] for snake in session['snakes'].values()])
            for session in recent_sessions
        ])

        report = f"""
AI Learning Progress Report
==========================

Recent Performance (Last 10 sessions):
- Average Survival Time: {avg_survival:.2f} seconds
- Average Decision Quality: {avg_decision_quality:.2%}
- Total Training Sessions: {len(self.session_data)}

Individual Snake Performance:
"""

        # Individual snake statistics
        for session in recent_sessions[-1:]:  # Most recent session
            for snake_id, stats in session['snakes'].items():
                report += f"""
Snake {snake_id}:
  - Survival Time: {stats['survival_time']:.2f}s
  - Decision Quality: {stats['decision_quality']:.2%}
  - Training Samples: {stats['training_samples']}
  - Model Trained: {stats['model_trained']}
"""

        return report
```

---

## 4. Advanced Feature Implementation

### 4.1 Multi-System Feature Integration

```python
def extract_advanced_survival_features(self, snake):
    """Extract features from advanced survival systems"""
    features = {}

    # Health system features (when implemented)
    if hasattr(snake, 'health_component'):
        health = snake.health_component
        features['health_percentage'] = health.current_hp / health.max_hp
        features['health_regen_rate'] = health.get_regeneration_rate()
        features['damage_sources_active'] = len(health.active_damage_sources)
        features['time_since_damage'] = time.time() - health.last_damage_time
    else:
        # Default values for non-implemented systems
        features['health_percentage'] = 1.0
        features['health_regen_rate'] = 0.0
        features['damage_sources_active'] = 0.0
        features['time_since_damage'] = 1.0

    # Energy system features (when implemented)
    if hasattr(snake, 'energy_component'):
        energy = snake.energy_component
        features['energy_percentage'] = energy.current_energy / energy.max_energy
        features['energy_state'] = energy.get_state_value()  # 0-3 for states
        features['sprint_available'] = 1.0 if energy.can_sprint() else 0.0
        features['energy_regen_rate'] = energy.get_regeneration_rate()
    else:
        features['energy_percentage'] = 1.0
        features['energy_state'] = 2.0  # Normal state
        features['sprint_available'] = 1.0
        features['energy_regen_rate'] = 0.1

    # Territory system features (when implemented)
    if hasattr(self.game_state, 'territory_system'):
        territory_data = self._analyze_territory_situation(snake)
        features.update(territory_data)
    else:
        features['owned_territories'] = 0.0
        features['territory_value'] = 0.0
        features['territorial_threats'] = 0.0

    return features

def _analyze_territory_situation(self, snake):
    """Analyze territorial control and opportunities"""
    features = {}

    territory_system = self.game_state.territory_system

    # Current territorial holdings
    owned_territories = territory_system.get_snake_territories(snake)
    features['owned_territories'] = min(len(owned_territories) / 3.0, 1.0)

    # Territory value assessment
    total_value = sum(territory.get_strategic_value() for territory in owned_territories)
    features['territory_value'] = min(total_value / 10.0, 1.0)

    # Territorial threats
    contested_territories = [t for t in owned_territories if t.is_contested()]
    features['territorial_threats'] = len(contested_territories) / max(len(owned_territories), 1)

    # Expansion opportunities
    nearby_territories = territory_system.get_claimable_territories_near(snake.head, 150)
    features['territory_opportunities'] = min(len(nearby_territories) / 5.0, 1.0)

    return features
```

---

## 5. Testing and Validation

### 5.1 AI Testing Framework

```python
class AITestingFramework:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.test_scenarios = []
        self.test_results = []

    def create_test_scenario(self, name, setup_function, success_criteria):
        """Create a standardized test scenario"""
        scenario = {
            'name': name,
            'setup': setup_function,
            'success_criteria': success_criteria,
            'runs': []
        }
        self.test_scenarios.append(scenario)

    def run_scenario_tests(self, scenario_name, num_runs=10):
        """Run multiple instances of a test scenario"""
        scenario = next(s for s in self.test_scenarios if s['name'] == scenario_name)

        results = []
        for run_id in range(num_runs):
            # Setup test environment
            scenario['setup'](self.game_manager)

            # Run simulation
            start_time = time.time()
            while self.game_manager.is_running() and time.time() - start_time < 300:  # 5 min max
                self.game_manager.update(1/60)  # 60 FPS simulation

            # Evaluate results
            success = scenario['success_criteria'](self.game_manager)
            ai_stats = self.game_manager.get_ai_statistics()

            results.append({
                'run_id': run_id,
                'success': success,
                'duration': time.time() - start_time,
                'ai_stats': ai_stats
            })

        scenario['runs'] = results
        return self._analyze_scenario_results(scenario)

    def _analyze_scenario_results(self, scenario):
        """Analyze test scenario results"""
        runs = scenario['runs']
        success_rate = sum(1 for run in runs if run['success']) / len(runs)
        avg_duration = np.mean([run['duration'] for run in runs])

        # Analyze AI performance across runs
        all_survival_times = []
        all_decision_qualities = []

        for run in runs:
            for snake_stats in run['ai_stats'].values():
                all_survival_times.append(snake_stats['survival_time'])
                all_decision_qualities.append(snake_stats['decision_quality'])

        analysis = {
            'scenario_name': scenario['name'],
            'success_rate': success_rate,
            'avg_duration': avg_duration,
            'avg_survival_time': np.mean(all_survival_times),
            'avg_decision_quality': np.mean(all_decision_qualities),
            'runs_completed': len(runs)
        }

        return analysis

# Example test scenarios
def setup_survival_test(game_manager):
    """Setup basic survival test scenario"""
    game_manager.reset()
    # Create single snake in center
    snake = game_manager.create_snake("test_snake")
    snake.position = Vector2(400, 300)  # Center of 800x600 screen
    # Add some environmental challenges
    game_manager.spawn_black_hole(Vector2(200, 200))
    game_manager.spawn_food_items(10)

def survival_success_criteria(game_manager):
    """Success criteria: survive for at least 2 minutes"""
    test_snake = game_manager.get_snake("test_snake")
    if test_snake and test_snake.is_alive:
        survival_time = time.time() - test_snake.birth_time
        return survival_time >= 120  # 2 minutes
    return False
```

This practical implementation guide provides concrete code examples for building the advanced AI system. The key points are:

1. **Modular Feature Extraction**: Organized, efficient feature extraction with caching
2. **Enhanced Decision Making**: Improved AI with exploration, training, and performance tracking
3. **Real-time Integration**: Seamless integration with the game loop
4. **Performance Monitoring**: Comprehensive tracking and reporting of AI learning progress
5. **Testing Framework**: Standardized testing for validating AI behavior

The implementation is designed to be incrementally deployable - you can start with the enhanced feature extraction and gradually add more sophisticated components as the advanced survival systems are implemented.
