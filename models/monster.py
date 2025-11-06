"""
Monster model extending the Character base class.
Follows Liskov Substitution Principle and Interface Segregation.
"""

from .character import Character


class Monster(Character):
    """
    Monster character class.
    Implements the attack method specific to monsters.
    """

    def __init__(self, name: str, health: int, attack: int):
        """
        Initialize a monster with given stats.

        Args:
            name: Monster name
            health: Health points
            attack: Attack damage
        """
        super().__init__(name, health, attack)

    def attack(self, enemy) -> None:
        """
        Attack an enemy, dealing damage equal to monster's attack stat.

        Args:
            enemy: Enemy to attack (must have health attribute)
        """
        enemy.take_damage(self.attack)