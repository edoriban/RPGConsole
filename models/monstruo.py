"""
Monster model extending the Personaje base class.
Follows Liskov Substitution Principle and Interface Segregation.
"""

from .personaje import Personaje


class Monstruo(Personaje):
    """
    Monster character class.
    Implements the attack method specific to monsters.
    """

    def __init__(self, nombre: str, vidas: int, ataque: int):
        """
        Initialize a monster with given stats.

        Args:
            nombre: Monster name
            vidas: Health points
            ataque: Attack damage
        """
        super().__init__(nombre, vidas, ataque)

    def atacar(self, enemigo) -> None:
        """
        Attack an enemy, dealing damage equal to monster's attack stat.

        Args:
            enemigo: Enemy to attack (must have vidas attribute)
        """
        enemigo.recibir_dano(self.ataque)