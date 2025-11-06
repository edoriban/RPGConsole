"""
Consumable items that can be used once and are depleted.
Follows Open/Closed Principle - can be extended with new consumable types.
"""

from .item import Item
from models.character import Character


class ConsumableItem(Item):
    """
    Base class for consumable items (potions, food, scrolls, etc.).
    These items are used once and then removed from inventory.
    """

    def __init__(self, name: str, description: str, value: int = 0, rarity: str = "common"):
        """
        Initialize a consumable item.

        Args:
            name: Item name
            description: Item description
            value: Monetary value
            rarity: Item rarity
        """
        super().__init__(name, description, value, rarity)

    def can_use(self, target) -> bool:
        """
        Check if the consumable can be used.
        Default implementation allows use on any living character.

        Args:
            target: The target character

        Returns:
            True if can be used, False otherwise
        """
        return isinstance(target, Character) and target.is_alive()


class HealthPotion(ConsumableItem):
    """
    Health potion that restores HP to the target.
    """

    def __init__(self, heal_amount: int = 50, name: str = "Health Potion",
                 description: str = "Restores 50 HP", value: int = 25, rarity: str = "common"):
        """
        Initialize a health potion.

        Args:
            heal_amount: Amount of HP to restore
            name: Item name
            description: Item description
            value: Monetary value
            rarity: Item rarity
        """
        super().__init__(name, description, value, rarity)
        self.heal_amount = heal_amount

    def use(self, target) -> bool:
        """
        Use the health potion on the target.

        Args:
            target: Character to heal

        Returns:
            True if healing was successful, False otherwise
        """
        if not self.can_use(target):
            return False

        old_health = target.health
        target.health = min(target.health + self.heal_amount, 100)  # Cap at 100 HP for now
        actual_heal = target.health - old_health

        print(f"{target.name} recovers {actual_heal} HP!")
        return True

    def can_use(self, target) -> bool:
        """
        Check if health potion can be used.
        Can only be used if target is not at full health.

        Args:
            target: The target character

        Returns:
            True if can be used, False otherwise
        """
        return (super().can_use(target) and
                target.health < 100)  # Assuming 100 is max HP


class ManaPotion(ConsumableItem):
    """
    Mana potion that restores MP to the target.
    Placeholder for future magic system.
    """

    def __init__(self, mana_amount: int = 30, name: str = "Mana Potion",
                 description: str = "Restores 30 MP", value: int = 30, rarity: str = "uncommon"):
        """
        Initialize a mana potion.

        Args:
            mana_amount: Amount of MP to restore
            name: Item name
            description: Item description
            value: Monetary value
            rarity: Item rarity
        """
        super().__init__(name, description, value, rarity)
        self.mana_amount = mana_amount

    def use(self, target) -> bool:
        """
        Use the mana potion on the target.
        Currently just a placeholder - no mana system implemented yet.

        Args:
            target: Character to restore mana to

        Returns:
            True (placeholder implementation)
        """
        if not self.can_use(target):
            return False

        print(f"{target.name} feels refreshed! (Mana system not yet implemented)")
        return True


class Food(ConsumableItem):
    """
    Food item that provides small healing and can be used outside combat.
    """

    def __init__(self, heal_amount: int = 20, name: str = "Bread",
                 description: str = "Restores 20 HP", value: int = 5, rarity: str = "common"):
        """
        Initialize a food item.

        Args:
            heal_amount: Amount of HP to restore
            name: Item name
            description: Item description
            value: Monetary value
            rarity: Item rarity
        """
        super().__init__(name, description, value, rarity)
        self.heal_amount = heal_amount

    def use(self, target) -> bool:
        """
        Use the food item on the target.

        Args:
            target: Character to feed

        Returns:
            True if feeding was successful, False otherwise
        """
        if not self.can_use(target):
            return False

        old_health = target.health
        target.health = min(target.health + self.heal_amount, 100)
        actual_heal = target.health - old_health

        print(f"{target.name} eats the {self.name} and recovers {actual_heal} HP!")
        return True