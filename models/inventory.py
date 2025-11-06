"""
Inventory system for managing hero items.
Follows Single Responsibility Principle - only handles inventory operations.
"""

from typing import List, Dict, Optional, Any
from collections import defaultdict
from .items.item import Item
from .items.consumable import HealthPotion, Food
from .items.equipment import Weapon, Armor, create_starter_sword, create_leather_armor


class Inventory:
    """
    Inventory system for managing items.
    Supports stacking for consumables and individual items for equipment.
    """

    def __init__(self, max_slots: int = 20):
        """
        Initialize inventory.

        Args:
            max_slots: Maximum number of inventory slots
        """
        self.max_slots = max_slots
        self.items: Dict[str, List[Item]] = defaultdict(list)
        self.gold = 0

    def add_item(self, item: Item) -> bool:
        """
        Add an item to inventory.

        Args:
            item: Item to add

        Returns:
            True if item was added, False if inventory is full
        """
        if self.get_total_slots_used() >= self.max_slots:
            return False

        self.items[item.name].append(item)
        return True

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Remove items from inventory.

        Args:
            item_name: Name of item to remove
            quantity: Number of items to remove

        Returns:
            True if items were removed, False if not enough items
        """
        if item_name not in self.items or len(self.items[item_name]) < quantity:
            return False

        for _ in range(quantity):
            self.items[item_name].pop()

        if not self.items[item_name]:
            del self.items[item_name]

        return True

    def get_item(self, item_name: str) -> Optional[Item]:
        """
        Get a single item from inventory (for use/consumption).

        Args:
            item_name: Name of item to get

        Returns:
            Item instance or None if not found
        """
        if item_name in self.items and self.items[item_name]:
            return self.items[item_name][0]
        return None

    def get_all_items(self) -> List[Item]:
        """
        Get all items in inventory (flattened list).

        Returns:
            List of all items
        """
        all_items = []
        for item_list in self.items.values():
            all_items.extend(item_list)
        return all_items

    def get_unique_items(self) -> Dict[str, int]:
        """
        Get unique items with their quantities.

        Returns:
            Dictionary of item names to quantities
        """
        return {name: len(items) for name, items in self.items.items()}

    def get_total_slots_used(self) -> int:
        """
        Get total number of inventory slots used.

        Returns:
            Number of slots used
        """
        return sum(len(items) for items in self.items.values())

    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """
        Check if inventory has enough of an item.

        Args:
            item_name: Name of item to check
            quantity: Required quantity

        Returns:
            True if has enough items, False otherwise
        """
        return item_name in self.items and len(self.items[item_name]) >= quantity

    def add_gold(self, amount: int) -> None:
        """
        Add gold to inventory.

        Args:
            amount: Amount of gold to add
        """
        self.gold += amount

    def remove_gold(self, amount: int) -> bool:
        """
        Remove gold from inventory.

        Args:
            amount: Amount of gold to remove

        Returns:
            True if gold was removed, False if insufficient gold
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def get_consumables(self) -> List[Item]:
        """
        Get all consumable items.

        Returns:
            List of consumable items
        """
        from .items.consumable import ConsumableItem
        return [item for item in self.get_all_items()
                if isinstance(item, ConsumableItem)]

    def get_equipment(self) -> List[Item]:
        """
        Get all equipment items.

        Returns:
            List of equipment items
        """
        from .items.equipment import Equipment
        return [item for item in self.get_all_items()
                if isinstance(item, Equipment)]

    def initialize_starter_gear(self) -> None:
        """Add starter equipment to new heroes."""
        self.add_item(create_starter_sword())
        self.add_item(create_leather_armor())
        self.add_item(HealthPotion())
        self.add_item(Food())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert inventory to dictionary for serialization.

        Returns:
            Dictionary representation of inventory
        """
        return {
            "max_slots": self.max_slots,
            "gold": self.gold,
            "items": {name: [item.to_dict() for item in items]
                     for name, items in self.items.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Inventory':
        """
        Create inventory from dictionary.

        Args:
            data: Dictionary containing inventory data

        Returns:
            Inventory instance
        """
        inventory = cls(max_slots=data.get("max_slots", 20))
        inventory.gold = data.get("gold", 0)

        # Reconstruct items (simplified - would need full item factory)
        for name, item_dicts in data.get("items", {}).items():
            for item_dict in item_dicts:
                # This is a simplified reconstruction
                # In a full implementation, you'd have an item factory
                if item_dict.get("type") == "HealthPotion":
                    inventory.add_item(HealthPotion())
                elif item_dict.get("type") == "Weapon":
                    # Simplified reconstruction
                    inventory.add_item(create_starter_sword())
                # Add other item types as needed

        return inventory

    def __str__(self) -> str:
        """String representation of inventory."""
        lines = [f"Inventory ({self.get_total_slots_used()}/{self.max_slots} slots):"]
        lines.append(f"Gold: {self.gold}")

        if not self.items:
            lines.append("  (empty)")
        else:
            for name, items in self.items.items():
                quantity = len(items)
                item = items[0]
                lines.append(f"  {item} x{quantity}")

        return "\n".join(lines)