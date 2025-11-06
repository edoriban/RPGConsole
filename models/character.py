"""
Character model following SOLID principles.
Single Responsibility: Handle character attributes and basic actions.
Open/Closed: Can be extended through inheritance.
"""

from abc import ABC, abstractmethod


class Character(ABC):
    """
    Abstract base class for all characters in the game.
    Follows Single Responsibility Principle by only handling character state.
    """

    def __init__(self, name: str, health: int, attack: int):
        """
        Initialize a character with basic attributes.

        Args:
            name: Character name
            health: Health points
            attack: Attack damage
        """
        self.name = name
        self.health = health
        self.attack = attack
        self.is_defending = False

    @abstractmethod
    def attack(self, enemy) -> None:
        """
        Abstract method for attacking an enemy.
        Must be implemented by concrete subclasses.
        """
        pass

    def defend(self) -> None:
        """
        Set defensive stance.
        Follows Open/Closed Principle - can be extended by subclasses.
        """
        self.is_defending = True

    def take_damage(self, damage: int) -> None:
        """
        Apply damage to the character.

        Args:
            damage: Amount of damage to apply
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        """
        Check if character is still alive.

        Returns:
            True if character has health > 0, False otherwise
        """
        return self.health > 0

    def reset_defense(self) -> None:
        """Reset defensive stance after a turn."""
        self.is_defending = False