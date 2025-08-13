# energy_health_system.py: Core Energy and Health management systems
import time
from enum import Enum
from typing import List, Tuple, Optional


class EnergyState(Enum):
    """Energy state categories affecting performance"""

    ENERGIZED = "energized"  # 80-100%
    NORMAL = "normal"  # 40-79%
    TIRED = "tired"  # 20-39%
    EXHAUSTED = "exhausted"  # 0-19%


class EnergyComponent:
    """Manages energy/stamina for entities"""

    def __init__(self, max_energy=100):
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.last_movement_time = 0
        self.sprint_active = False
        self.energy_regeneration_rate = 0.15  # Base regeneration rate

        # Energy consumption rates
        self.movement_cost = 0.1  # per second
        self.sprint_cost = 0.3  # per second
        self.combat_cost = 2.0  # per action
        self.ability_cost = 5.0  # per use
        self.territory_defense_cost = 1.0  # per second

    def get_energy_state(self) -> EnergyState:
        """Get current energy state based on percentage"""
        percentage = (self.current_energy / self.max_energy) * 100

        if percentage >= 80:
            return EnergyState.ENERGIZED
        elif percentage >= 40:
            return EnergyState.NORMAL
        elif percentage >= 20:
            return EnergyState.TIRED
        else:
            return EnergyState.EXHAUSTED

    def get_energy_percentage(self) -> float:
        """Get energy as percentage (0.0 to 1.0)"""
        return self.current_energy / self.max_energy

    def can_sprint(self) -> bool:
        """Check if entity has enough energy to sprint"""
        return self.get_energy_state() != EnergyState.EXHAUSTED

    def can_use_ability(self) -> bool:
        """Check if entity has enough energy for special abilities"""
        return self.current_energy >= self.ability_cost

    def consume_energy(self, amount: float) -> bool:
        """Consume energy, return True if successful"""
        if self.current_energy >= amount:
            self.current_energy = max(0, self.current_energy - amount)
            return True
        return False

    def regenerate_energy(self, dt: float, bonus_rate: float = 0.0):
        """Regenerate energy over time"""
        total_rate = self.energy_regeneration_rate + bonus_rate
        self.current_energy = min(
            self.max_energy, self.current_energy + total_rate * dt
        )

    def is_resting(self, current_time: float) -> bool:
        """Check if entity is resting (not moved for 2+ seconds)"""
        return current_time - self.last_movement_time >= 2.0

    def update_movement_time(self, current_time: float):
        """Update last movement time"""
        self.last_movement_time = current_time


class HealthComponent:
    """Manages health/HP for entities"""

    def __init__(self, max_hp=10):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.damage_sources = []  # List of (source_name, damage_per_second, duration)
        self.healing_sources = []  # List of (source_name, healing_per_second, duration)
        self.last_damage_time = 0
        self.immunity_duration = 0  # Brief immunity after taking damage
        self.natural_regen_rate = 0.1  # HP per second in safe zones

    def get_health_percentage(self) -> float:
        """Get health as percentage (0.0 to 1.0)"""
        return self.current_hp / self.max_hp

    def is_alive(self) -> bool:
        """Check if entity is still alive"""
        return self.current_hp > 0

    def is_damaged(self) -> bool:
        """Check if entity has taken damage"""
        return self.current_hp < self.max_hp

    def take_damage(self, amount: float, source: str) -> bool:
        """Apply damage, return True if damage was taken"""
        if self.immunity_duration <= 0:
            self.current_hp = max(0, self.current_hp - amount)
            self.last_damage_time = time.time()
            self.immunity_duration = 0.5  # 0.5 second immunity
            return True
        return False

    def heal(self, amount: float) -> float:
        """Heal damage, return actual amount healed"""
        old_hp = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - old_hp

    def add_damage_source(
        self, source_name: str, damage_per_second: float, duration: float
    ):
        """Add a damage over time effect"""
        self.damage_sources.append(
            {
                "name": source_name,
                "damage_per_second": damage_per_second,
                "duration": duration,
                "start_time": time.time(),
            }
        )

    def add_healing_source(
        self, source_name: str, healing_per_second: float, duration: float
    ):
        """Add a healing over time effect"""
        self.healing_sources.append(
            {
                "name": source_name,
                "healing_per_second": healing_per_second,
                "duration": duration,
                "start_time": time.time(),
            }
        )

    def update(self, dt: float, in_safe_zone: bool = False):
        """Update health with damage/healing over time effects"""
        current_time = time.time()

        # Update immunity
        if self.immunity_duration > 0:
            self.immunity_duration -= dt

        # Process damage over time effects
        active_damage = []
        for source in self.damage_sources:
            elapsed = current_time - source["start_time"]
            if elapsed < source["duration"]:
                self.take_damage(source["damage_per_second"] * dt, source["name"])
                active_damage.append(source)
        self.damage_sources = active_damage

        # Process healing over time effects
        active_healing = []
        for source in self.healing_sources:
            elapsed = current_time - source["start_time"]
            if elapsed < source["duration"]:
                self.heal(source["healing_per_second"] * dt)
                active_healing.append(source)
        self.healing_sources = active_healing

        # Natural regeneration in safe zones
        if in_safe_zone and len(self.damage_sources) == 0:
            self.heal(self.natural_regen_rate * dt)


class EnergyHealthManager:
    """Coordinates energy and health systems for game entities"""

    def __init__(self):
        self.entities = {}  # entity_id -> (energy_component, health_component)

    def add_entity(self, entity_id: str, max_energy: int = 100, max_hp: int = 10):
        """Add an entity to the system"""
        energy_comp = EnergyComponent(max_energy)
        health_comp = HealthComponent(max_hp)
        self.entities[entity_id] = (energy_comp, health_comp)
        return energy_comp, health_comp

    def remove_entity(self, entity_id: str):
        """Remove an entity from the system"""
        if entity_id in self.entities:
            del self.entities[entity_id]

    def get_components(
        self, entity_id: str
    ) -> Tuple[Optional[EnergyComponent], Optional[HealthComponent]]:
        """Get energy and health components for an entity"""
        if entity_id in self.entities:
            return self.entities[entity_id]
        return None, None

    def update_all(self, dt: float):
        """Update all entities' energy and health"""
        for entity_id, (energy, health) in self.entities.items():
            # Update health (assuming safe zone for now, will be overridden by specific conditions)
            health.update(dt, in_safe_zone=True)

            # Energy regeneration (base rate, bonuses applied elsewhere)
            current_time = time.time()
            if energy.is_resting(current_time):
                energy.regenerate_energy(dt)

    def apply_movement_energy_cost(
        self, entity_id: str, dt: float, is_sprinting: bool = False
    ) -> bool:
        """Apply energy cost for movement, return True if movement is allowed"""
        energy, _ = self.get_components(entity_id)
        if not energy:
            return True  # Allow movement if no energy component

        cost = energy.sprint_cost if is_sprinting else energy.movement_cost
        energy_needed = cost * dt

        if energy.consume_energy(energy_needed):
            energy.update_movement_time(time.time())
            return True
        return False

    def get_movement_speed_multiplier(self, entity_id: str) -> float:
        """Get speed multiplier based on energy state"""
        energy, _ = self.get_components(entity_id)
        if not energy:
            return 1.0

        state = energy.get_energy_state()
        if state == EnergyState.EXHAUSTED:
            return 0.5  # Half speed when exhausted
        elif state == EnergyState.TIRED:
            return 0.8  # Reduced speed when tired
        else:
            return 1.0  # Normal speed

    def get_status_for_ui(self, entity_id: str) -> dict:
        """Get energy and health status for UI display"""
        energy, health = self.get_components(entity_id)

        if not energy or not health:
            return {}

        return {
            "energy_percentage": energy.get_energy_percentage(),
            "health_percentage": health.get_health_percentage(),
            "energy_state": energy.get_energy_state().value,
            "is_damaged": health.is_damaged(),
            "is_alive": health.is_alive(),
            "can_sprint": energy.can_sprint(),
            "can_use_ability": energy.can_use_ability(),
        }
