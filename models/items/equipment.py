"""
Equipment items that can be equipped for stat bonuses.
Follows Interface Segregation Principle with specific equipment interfaces.
"""

from abc import ABC, abstractmethod
from typing import Dict
from .item import Item
from models.character import Character


class Equippable(ABC):
    """
    Interface for items that can be equipped.
    Follows Interface Segregation Principle.
    """

    @abstractmethod
    def get_stat_bonuses(self) -> Dict[str, int]:
        """
        Get the stat bonuses provided by this equipment.

        Returns:
            Dictionary of stat bonuses (e.g., {'attack': 5, 'defense': 3})
        """
        pass

    @abstractmethod
    def can_equip(self, character: Character) -> bool:
        """
        Check if the character can equip this item.

        Args:
            character: Character attempting to equip

        Returns:
            True if can equip, False otherwise
        """
        pass


class Equipment(Item, Equippable):
    """
    Base class for equipment items (weapons, armor, accessories).
    Equipment provides ongoing stat bonuses when equipped.
    """

    def __init__(self, name: str, description: str, value: int = 0, rarity: str = "common",
                 required_level: int = 1):
        """
        Initialize equipment.

        Args:
            name: Equipment name
            description: Equipment description
            value: Monetary value
            rarity: Item rarity
            required_level: Minimum level required to equip
        """
        super().__init__(name, description, value, rarity)
        self.required_level = required_level
        self.equipped = False

    def use(self, target) -> bool:
        """
        Equipment is used by equipping/unequipping.
        This method handles the toggle behavior.

        Args:
            target: Character to equip/unequip on

        Returns:
            True if action was successful, False otherwise
        """
        if not self.can_use(target):
            return False

        if self.equipped:
            self.unequip(target)
        else:
            self.equip(target)

        return True

    def can_use(self, target) -> bool:
        """
        Check if equipment can be used (equipped/unequipped).

        Args:
            target: Character attempting to use

        Returns:
            True if can be used, False otherwise
        """
        return isinstance(target, Character) and target.is_alive()

    @abstractmethod
    def equip(self, character: Character) -> None:
        """
        Equip the item on the character.

        Args:
            character: Character to equip on
        """
        pass

    @abstractmethod
    def unequip(self, character: Character) -> None:
        """
        Unequip the item from the character.

        Args:
            character: Character to unequip from
        """
        pass

    def can_equip(self, character: Character) -> bool:
        """
        Check if character can equip this item.

        Args:
            character: Character attempting to equip

        Returns:
            True if can equip, False otherwise
        """
        # Check if character has required level
        if hasattr(character, 'level'):
            return character.level >= self.required_level
        return True  # No level system yet, allow equipping


class Weapon(Equipment):
    """
    Weapon equipment that provides attack bonuses.
    """

    def __init__(self, name: str, description: str, attack_bonus: int,
                 value: int = 0, rarity: str = "common", required_level: int = 1):
        """
        Initialize a weapon.

        Args:
            name: Weapon name
            description: Weapon description
            attack_bonus: Attack damage bonus
            value: Monetary value
            rarity: Item rarity
            required_level: Minimum level required
        """
        super().__init__(name, description, value, rarity, required_level)
        self.attack_bonus = attack_bonus

    def get_stat_bonuses(self) -> Dict[str, int]:
        """
        Get weapon stat bonuses.

        Returns:
            Dictionary with attack bonus
        """
        return {"attack": self.attack_bonus}

    def equip(self, character: Character) -> None:
        """
        Equip weapon on character.

        Args:
            character: Character to equip weapon on
        """
        if self.can_equip(character):
            character.attack += self.attack_bonus
            self.equipped = True
            print(f"{character.name} equips {self.name} (+{self.attack_bonus} attack)!")
        else:
            print(f"{character.name} cannot equip {self.name} (level {self.required_level} required)!")

    def unequip(self, character: Character) -> None:
        """
        Unequip weapon from character.

        Args:
            character: Character to unequip weapon from
        """
        character.attack -= self.attack_bonus
        self.equipped = False
        print(f"{character.name} unequips {self.name} (-{self.attack_bonus} attack).")


class Armor(Equipment):
    """
    Armor equipment that provides defense bonuses.
    """

    def __init__(self, name: str, description: str, defense_bonus: int,
                 value: int = 0, rarity: str = "common", required_level: int = 1):
        """
        Initialize armor.

        Args:
            name: Armor name
            description: Armor description
            defense_bonus: Defense bonus
            value: Monetary value
            rarity: Item rarity
            required_level: Minimum level required
        """
        super().__init__(name, description, value, rarity, required_level)
        self.defense_bonus = defense_bonus

    def get_stat_bonuses(self) -> Dict[str, int]:
        """
        Get armor stat bonuses.

        Returns:
            Dictionary with defense bonus
        """
        return {"defense": self.defense_bonus}

    def equip(self, character: Character) -> None:
        """
        Equip armor on character.

        Args:
            character: Character to equip armor on
        """
        if self.can_equip(character):
            # For now, just add to attack as defense bonus (simplified)
            character.attack += self.defense_bonus
            self.equipped = True
            print(f"{character.name} equips {self.name} (+{self.defense_bonus} defense)!")
        else:
            print(f"{character.name} cannot equip {self.name} (level {self.required_level} required)!")

    def unequip(self, character: Character) -> None:
        """
        Unequip armor from character.

        Args:
            character: Character to unequip armor from
        """
        character.attack -= self.defense_bonus
        self.equipped = False
        print(f"{character.name} unequips {self.name} (-{self.defense_bonus} defense).")


# Predefined equipment items
def create_starter_sword() -> Weapon:
    """Create a basic starter sword."""
    return Weapon(
        name="Iron Sword",
        description="A basic iron sword for beginners",
        attack_bonus=5,
        value=50,
        rarity="common",
        required_level=1
    )


def create_health_potion() -> 'HealthPotion':
    """Create a basic health potion."""
    from .consumable import HealthPotion
    return HealthPotion()


def create_leather_armor() -> Armor:
    """Create basic leather armor."""
    return Armor(
        name="Leather Armor",
        description="Basic protection made from leather",
        defense_bonus=3,
        value=30,
        rarity="common",
        required_level=1
    )