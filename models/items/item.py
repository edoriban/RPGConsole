"""
Item base class following SOLID principles.
Defines the interface for all items in the game.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class Item(ABC):
    """
    Abstract base class for all items in the game.
    Follows Single Responsibility Principle - defines item interface.
    """

    def __init__(self, name: str, description: str, value: int = 0, rarity: str = "common"):
        """
        Initialize an item with basic properties.

        Args:
            name: Item name
            description: Item description
            value: Monetary value
            rarity: Item rarity (common, uncommon, rare, epic, legendary)
        """
        self.name = name
        self.description = description
        self.value = value
        self.rarity = rarity
        self.quantity = 1

    @abstractmethod
    def use(self, target) -> bool:
        """
        Abstract method for using the item.

        Args:
            target: The character using the item

        Returns:
            True if use was successful, False otherwise
        """
        pass

    @abstractmethod
    def can_use(self, target) -> bool:
        """
        Check if the item can be used on the target.

        Args:
            target: The potential target of the item

        Returns:
            True if item can be used, False otherwise
        """
        pass

    def get_rarity_color(self) -> str:
        """
        Get colorama color code based on item rarity.

        Returns:
            Colorama color string
        """
        colors = {
            "common": "",
            "uncommon": "\033[92m",  # Green
            "rare": "\033[94m",      # Blue
            "epic": "\033[95m",      # Magenta
            "legendary": "\033[93m"  # Yellow
        }
        return colors.get(self.rarity, "")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert item to dictionary for serialization.

        Returns:
            Dictionary representation of the item
        """
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "rarity": self.rarity,
            "quantity": self.quantity,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """
        Create item from dictionary (for deserialization).

        Args:
            data: Dictionary containing item data

        Returns:
            Item instance
        """
        return cls(
            name=data["name"],
            description=data["description"],
            value=data.get("value", 0),
            rarity=data.get("rarity", "common")
        )

    def __str__(self) -> str:
        """String representation of the item."""
        color = self.get_rarity_color()
        reset = "\033[0m" if color else ""
        return f"{color}{self.name}{reset} - {self.description}"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return f"{self.__class__.__name__}(name='{self.name}', rarity='{self.rarity}', quantity={self.quantity})"