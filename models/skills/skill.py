"""
Skill system for RPG characters.
Skills are special abilities that can be learned and used in combat.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from models.character import Character


class Skill(ABC):
    """
    Abstract base class for all skills in the game.
    Skills are special abilities that characters can learn and use.
    """

    def __init__(self, name: str, description: str, required_level: int = 1,
                 mana_cost: int = 0, cooldown: int = 0):
        """
        Initialize a skill.

        Args:
            name: Skill name
            description: Skill description
            required_level: Minimum level required to learn
            mana_cost: Mana points required to use (future feature)
            cooldown: Turns before skill can be used again
        """
        self.name = name
        self.description = description
        self.required_level = required_level
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.current_cooldown = 0

    @abstractmethod
    def can_use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Check if the skill can be used.

        Args:
            user: Character using the skill
            target: Target of the skill (if applicable)

        Returns:
            True if skill can be used, False otherwise
        """
        pass

    @abstractmethod
    def use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Execute the skill.

        Args:
            user: Character using the skill
            target: Target of the skill (if applicable)

        Returns:
            True if skill was used successfully, False otherwise
        """
        pass

    def is_on_cooldown(self) -> bool:
        """
        Check if skill is currently on cooldown.

        Returns:
            True if on cooldown, False otherwise
        """
        return self.current_cooldown > 0

    def reduce_cooldown(self) -> None:
        """Reduce cooldown by 1 turn."""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def reset_cooldown(self) -> None:
        """Reset cooldown to maximum."""
        self.current_cooldown = self.cooldown

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert skill to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "description": self.description,
            "required_level": self.required_level,
            "mana_cost": self.mana_cost,
            "cooldown": self.cooldown,
            "current_cooldown": self.current_cooldown,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        """
        Create skill from dictionary.

        Args:
            data: Dictionary containing skill data

        Returns:
            Skill instance
        """
        return cls(
            name=data["name"],
            description=data["description"],
            required_level=data.get("required_level", 1),
            mana_cost=data.get("mana_cost", 0),
            cooldown=data.get("cooldown", 0)
        )

    def __str__(self) -> str:
        """String representation of the skill."""
        cooldown_info = f" (Cooldown: {self.current_cooldown})" if self.current_cooldown > 0 else ""
        return f"{self.name} - {self.description}{cooldown_info}"


class OffensiveSkill(Skill):
    """
    Skills that deal damage to enemies.
    """

    def __init__(self, name: str, description: str, damage: int,
                 required_level: int = 1, mana_cost: int = 0, cooldown: int = 0):
        """
        Initialize an offensive skill.

        Args:
            name: Skill name
            description: Skill description
            damage: Base damage dealt
            required_level: Minimum level required
            mana_cost: Mana cost
            cooldown: Cooldown turns
        """
        super().__init__(name, description, required_level, mana_cost, cooldown)
        self.damage = damage

    def can_use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Check if offensive skill can be used.

        Args:
            user: Character using the skill
            target: Enemy target

        Returns:
            True if can be used, False otherwise
        """
        if not target or not target.is_alive():
            return False
        if self.is_on_cooldown():
            return False
        # Add mana check here when mana system is implemented
        return True

    def use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Execute offensive skill.

        Args:
            user: Character using the skill
            target: Enemy target

        Returns:
            True if successful, False otherwise
        """
        if not self.can_use(user, target):
            return False

        # Calculate damage (can be modified by character stats later)
        actual_damage = self.damage
        target.take_damage(actual_damage)

        print(f"{user.name} uses {self.name}!")
        print(f"{target.name} takes {actual_damage} damage!")

        self.reset_cooldown()
        return True


class DefensiveSkill(Skill):
    """
    Skills that provide defensive benefits.
    """

    def __init__(self, name: str, description: str, defense_bonus: int,
                 required_level: int = 1, mana_cost: int = 0, cooldown: int = 0):
        """
        Initialize a defensive skill.

        Args:
            name: Skill name
            description: Skill description
            defense_bonus: Defense bonus provided
            required_level: Minimum level required
            mana_cost: Mana cost
            cooldown: Cooldown turns
        """
        super().__init__(name, description, required_level, mana_cost, cooldown)
        self.defense_bonus = defense_bonus

    def can_use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Check if defensive skill can be used.

        Args:
            user: Character using the skill
            target: Not used for defensive skills

        Returns:
            True if can be used, False otherwise
        """
        if self.is_on_cooldown():
            return False
        return user.is_alive()

    def use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Execute defensive skill.

        Args:
            user: Character using the skill
            target: Not used for defensive skills

        Returns:
            True if successful, False otherwise
        """
        if not self.can_use(user):
            return False

        # For now, just set defense flag (can be expanded)
        user.defend()

        print(f"{user.name} uses {self.name}!")
        print(f"Defense increased by {self.defense_bonus}!")

        self.reset_cooldown()
        return True


class HealingSkill(Skill):
    """
    Skills that restore health.
    """

    def __init__(self, name: str, description: str, heal_amount: int,
                 required_level: int = 1, mana_cost: int = 0, cooldown: int = 0):
        """
        Initialize a healing skill.

        Args:
            name: Skill name
            description: Skill description
            heal_amount: Amount of HP restored
            required_level: Minimum level required
            mana_cost: Mana cost
            cooldown: Cooldown turns
        """
        super().__init__(name, description, required_level, mana_cost, cooldown)
        self.heal_amount = heal_amount

    def can_use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Check if healing skill can be used.

        Args:
            user: Character using the skill
            target: Character to heal (defaults to user)

        Returns:
            True if can be used, False otherwise
        """
        heal_target = target or user
        if not heal_target.is_alive():
            return False
        if heal_target.health >= 100:  # Assuming 100 is max HP
            return False
        if self.is_on_cooldown():
            return False
        return True

    def use(self, user: Character, target: Optional[Character] = None) -> bool:
        """
        Execute healing skill.

        Args:
            user: Character using the skill
            target: Character to heal (defaults to user)

        Returns:
            True if successful, False otherwise
        """
        heal_target = target or user

        if not self.can_use(user, heal_target):
            return False

        old_health = heal_target.health
        heal_target.health = min(heal_target.health + self.heal_amount, 100)
        actual_heal = heal_target.health - old_health

        print(f"{user.name} uses {self.name}!")
        if heal_target != user:
            print(f"{heal_target.name} recovers {actual_heal} HP!")
        else:
            print(f"{user.name} recovers {actual_heal} HP!")

        self.reset_cooldown()
        return True


# Predefined skills
def create_power_strike() -> OffensiveSkill:
    """Create Power Strike skill."""
    return OffensiveSkill(
        name="Power Strike",
        description="A powerful strike dealing extra damage",
        damage=25,
        required_level=2,
        mana_cost=0,
        cooldown=2
    )


def create_shield_block() -> DefensiveSkill:
    """Create Shield Block skill."""
    return DefensiveSkill(
        name="Shield Block",
        description="Raise shield to block incoming attacks",
        defense_bonus=5,
        required_level=1,
        mana_cost=0,
        cooldown=1
    )


def create_healing_light() -> HealingSkill:
    """Create Healing Light skill."""
    return HealingSkill(
        name="Healing Light",
        description="Restore health with divine light",
        heal_amount=30,
        required_level=3,
        mana_cost=0,
        cooldown=3
    )