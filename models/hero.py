"""
Hero model extending the Character base class.
Follows Liskov Substitution Principle - can be used wherever Character is expected.
"""

from .character import Character


class Hero(Character):
    """
    Hero character class.
    Implements the attack method specific to heroes.
    """

    def __init__(self, name: str, health: int = 100, attack: int = 15):
        """
        Initialize a hero with default stats.

        Args:
            name: Hero name
            health: Health points (default: 100)
            attack: Attack damage (default: 15)
        """
        super().__init__(name, health, attack)

    def attack(self, enemy) -> None:
        """
        Attack an enemy, dealing damage equal to hero's attack stat.

        Args:
            enemy: Enemy to attack (must have health attribute)
        """
        enemy.take_damage(self.attack)