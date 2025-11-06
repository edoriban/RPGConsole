"""
Zone system for RPG world exploration.
Zones represent different areas the player can explore.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from models.monster import Monster
from models.items.item import Item
from data.monsters import get_monster_names, get_monster_stats


class Zone(ABC):
    """
    Abstract base class for game zones/areas.
    Zones are explorable areas with different characteristics.
    """

    def __init__(self, name: str, description: str, danger_level: int = 1):
        """
        Initialize a zone.

        Args:
            name: Zone name
            description: Zone description
            danger_level: Difficulty level (affects enemy strength)
        """
        self.name = name
        self.description = description
        self.danger_level = danger_level
        self.discovered = False
        self.visited = False

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """
        Get list of available actions in this zone.

        Returns:
            List of action names
        """
        pass

    @abstractmethod
    def explore(self) -> str:
        """
        Explore the zone and return description.

        Returns:
            Exploration result description
        """
        pass

    @abstractmethod
    def can_have_combat(self) -> bool:
        """
        Check if this zone can have random combat encounters.

        Returns:
            True if combat is possible, False otherwise
        """
        pass

    def generate_random_encounter(self) -> Optional[Monster]:
        """
        Generate a random monster encounter for this zone.

        Returns:
            Monster instance or None if no encounter
        """
        if not self.can_have_combat():
            return None

        # Base encounter chance
        encounter_chance = 0.3  # 30% chance

        # Modify chance based on danger level
        encounter_chance += (self.danger_level - 1) * 0.1

        import random
        if random.random() < encounter_chance:
            return self._create_zone_monster()
        return None

    @abstractmethod
    def _create_zone_monster(self) -> Monster:
        """
        Create a monster appropriate for this zone.

        Returns:
            Monster instance
        """
        pass

    def get_loot_table(self) -> List[Item]:
        """
        Get possible loot items for this zone.

        Returns:
            List of possible loot items
        """
        # Base implementation - can be overridden
        return []

    def mark_discovered(self) -> None:
        """Mark zone as discovered."""
        self.discovered = True

    def mark_visited(self) -> None:
        """Mark zone as visited."""
        self.visited = True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert zone to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "danger_level": self.danger_level,
            "discovered": self.discovered,
            "visited": self.visited,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Zone':
        """
        Create zone from dictionary.

        Args:
            data: Dictionary containing zone data

        Returns:
            Zone instance
        """
        zone = cls(
            name=data["name"],
            description=data["description"],
            danger_level=data.get("danger_level", 1)
        )
        zone.discovered = data.get("discovered", False)
        zone.visited = data.get("visited", False)
        return zone

    def __str__(self) -> str:
        """String representation of the zone."""
        status = ""
        if self.visited:
            status = " (Visited)"
        elif self.discovered:
            status = " (Discovered)"
        else:
            status = " (Unknown)"

        return f"{self.name}{status} - {self.description}"


class SafeZone(Zone):
    """
    Safe zones where no combat occurs (towns, safe areas).
    """

    def __init__(self, name: str, description: str):
        """Initialize a safe zone."""
        super().__init__(name, description, danger_level=0)

    def get_available_actions(self) -> List[str]:
        """Get available actions in safe zone."""
        return ["rest", "shop", "talk", "leave"]

    def explore(self) -> str:
        """Explore the safe zone."""
        return f"You explore {self.name}. It's a peaceful area where you can rest and prepare for your journey."

    def can_have_combat(self) -> bool:
        """Safe zones have no combat."""
        return False

    def _create_zone_monster(self) -> Monster:
        """Safe zones don't create monsters."""
        raise NotImplementedError("Safe zones don't have monsters")


class CombatZone(Zone):
    """
    Zones where combat encounters can occur.
    """

    def __init__(self, name: str, description: str, danger_level: int = 1,
                 monster_types: Optional[List[str]] = None):
        """
        Initialize a combat zone.

        Args:
            name: Zone name
            description: Zone description
            danger_level: Difficulty level
            monster_types: List of allowed monster types
        """
        super().__init__(name, description, danger_level)
        self.monster_types = monster_types or ["Goblin", "Ogre", "Orc", "Slime"]

    def get_available_actions(self) -> List[str]:
        """Get available actions in combat zone."""
        return ["explore", "search", "rest", "leave"]

    def explore(self) -> str:
        """Explore the combat zone."""
        return f"You venture deeper into {self.name}. The area seems dangerous, and you stay alert for any threats."

    def can_have_combat(self) -> bool:
        """Combat zones can have combat."""
        return True

    def _create_zone_monster(self) -> Monster:
        """
        Create a random monster for this zone.

        Returns:
            Monster instance scaled to zone danger level
        """
        import random

        # Filter available monsters
        available_monsters = [m for m in self.monster_types if m in get_monster_names()]
        if not available_monsters:
            available_monsters = get_monster_names()

        monster_name = random.choice(available_monsters)
        stats = get_monster_stats(monster_name)

        # Scale monster stats based on danger level
        scaled_health = stats["health"] + (self.danger_level - 1) * 10
        scaled_attack = stats["attack"] + (self.danger_level - 1) * 2

        return Monster(monster_name, scaled_health, scaled_attack)


# Predefined zones
def create_forest() -> CombatZone:
    """Create the peaceful forest zone."""
    return CombatZone(
        name="Peaceful Forest",
        description="A quiet forest with tall trees and winding paths",
        danger_level=1,
        monster_types=["Goblin", "Slime"]
    )


def create_cave() -> CombatZone:
    """Create the dark cave zone."""
    return CombatZone(
        name="Dark Cave",
        description="A mysterious cave with echoing chambers",
        danger_level=2,
        monster_types=["Goblin", "Ogre", "Orc"]
    )


def create_mountain() -> CombatZone:
    """Create the snowy mountain zone."""
    return CombatZone(
        name="Snowy Mountain",
        description="A towering mountain covered in snow",
        danger_level=3,
        monster_types=["Ogre", "Orc"]
    )


def create_castle() -> CombatZone:
    """Create the ancient castle zone."""
    return CombatZone(
        name="Ancient Castle",
        description="An old castle filled with secrets and dangers",
        danger_level=4,
        monster_types=["Orc", "Ogre"]
    )


def create_town() -> SafeZone:
    """Create the town safe zone."""
    return SafeZone(
        name="Peaceful Town",
        description="A quiet town where adventurers can rest and resupply"
    )