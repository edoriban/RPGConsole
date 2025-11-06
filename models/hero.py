"""
Hero model extending the Character base class.
Follows Liskov Substitution Principle - can be used wherever Character is expected.
Includes leveling, inventory, and progression systems.
"""

from .character import Character
from .inventory import Inventory


class Hero(Character):
    """
    Hero character class with leveling and inventory systems.
    Implements the attack method specific to heroes.
    """

    def __init__(self, name: str, health: int = 100, attack: int = 15):
        """
        Initialize a hero with default stats and progression systems.

        Args:
            name: Hero name
            health: Health points (default: 100)
            attack: Attack damage (default: 15)
        """
        super().__init__(name, health, attack)

        # Leveling system
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100
        self.skill_points = 0

        # Base stats (for leveling calculations)
        self.base_health = health
        self.base_attack = attack

        # Inventory system
        self.inventory = Inventory()
        self.inventory.initialize_starter_gear()

        # Equipment bonuses
        self.equipment_attack_bonus = 0
        self.equipment_defense_bonus = 0

    def attack(self, enemy) -> None:
        """
        Attack an enemy, dealing damage equal to hero's attack stat.

        Args:
            enemy: Enemy to attack (must have health attribute)
        """
        total_attack = self.attack + self.equipment_attack_bonus
        enemy.take_damage(total_attack)

    def gain_experience(self, amount: int) -> bool:
        """
        Gain experience points and check for level up.

        Args:
            amount: Experience points gained

        Returns:
            True if leveled up, False otherwise
        """
        self.experience += amount
        leveled_up = False

        while self.experience >= self.experience_to_next:
            self._level_up()
            leveled_up = True

        return leveled_up

    def _level_up(self) -> None:
        """
        Perform level up calculations and stat increases.
        """
        self.experience -= self.experience_to_next
        self.level += 1
        self.skill_points += 1

        # Increase stats
        health_increase = 10
        attack_increase = 2

        self.base_health += health_increase
        self.base_attack += attack_increase

        # Update current stats
        self.health += health_increase
        self.attack += attack_increase

        # Increase XP requirement for next level
        self.experience_to_next = int(self.experience_to_next * 1.5)

        print(f"🎉 {self.name} leveled up to level {self.level}!")
        print(f"   Health: +{health_increase} → {self.base_health}")
        print(f"   Attack: +{attack_increase} → {self.base_attack}")
        print(f"   Skill Points: +1 → {self.skill_points}")

    def equip_weapon(self, weapon) -> bool:
        """
        Equip a weapon and apply bonuses.

        Args:
            weapon: Weapon to equip

        Returns:
            True if equipped successfully, False otherwise
        """
        if weapon.can_equip(self):
            # Remove old weapon bonus if exists
            self.attack -= self.equipment_attack_bonus

            # Apply new weapon bonus
            bonuses = weapon.get_stat_bonuses()
            self.equipment_attack_bonus = bonuses.get("attack", 0)
            self.attack += self.equipment_attack_bonus

            return True
        return False

    def unequip_weapon(self, weapon) -> None:
        """
        Unequip a weapon and remove bonuses.

        Args:
            weapon: Weapon to unequip
        """
        self.attack -= self.equipment_attack_bonus
        self.equipment_attack_bonus = 0

    def get_total_attack(self) -> int:
        """
        Get total attack including equipment bonuses.

        Returns:
            Total attack value
        """
        return self.attack

    def get_inventory_summary(self) -> str:
        """
        Get a summary of hero's inventory.

        Returns:
            Formatted inventory string
        """
        return str(self.inventory)

    def use_item(self, item_name: str) -> bool:
        """
        Use an item from inventory.

        Args:
            item_name: Name of item to use

        Returns:
            True if item was used successfully, False otherwise
        """
        item = self.inventory.get_item(item_name)
        if item and item.use(self):
            self.inventory.remove_item(item_name, 1)
            return True
        return False

    def to_dict(self) -> dict:
        """
        Convert hero to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "health": self.health,
            "attack": self.attack,
            "level": self.level,
            "experience": self.experience,
            "experience_to_next": self.experience_to_next,
            "skill_points": self.skill_points,
            "base_health": self.base_health,
            "base_attack": self.base_attack,
            "inventory": self.inventory.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Hero':
        """
        Create hero from dictionary.

        Args:
            data: Dictionary containing hero data

        Returns:
            Hero instance
        """
        hero = cls(
            name=data["name"],
            health=data.get("base_health", 100),
            attack=data.get("base_attack", 15)
        )

        # Override with saved stats
        hero.health = data.get("health", hero.health)
        hero.attack = data.get("attack", hero.attack)
        hero.level = data.get("level", 1)
        hero.experience = data.get("experience", 0)
        hero.experience_to_next = data.get("experience_to_next", 100)
        hero.skill_points = data.get("skill_points", 0)
        hero.base_health = data.get("base_health", hero.base_health)
        hero.base_attack = data.get("base_attack", hero.base_attack)

        # Load inventory
        if "inventory" in data:
            hero.inventory = Inventory.from_dict(data["inventory"])

        return hero