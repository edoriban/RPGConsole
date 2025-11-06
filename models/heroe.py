"""
Hero model extending the Personaje base class.
Follows Liskov Substitution Principle - can be used wherever Personaje is expected.
"""

from .personaje import Personaje


class Heroe(Personaje):
    """
    Hero character class.
    Implements the attack method specific to heroes.
    """

    def __init__(self, nombre: str, vidas: int = 100, ataque: int = 15):
        """
        Initialize a hero with default stats.

        Args:
            nombre: Hero name
            vidas: Health points (default: 100)
            ataque: Attack damage (default: 15)
        """
        super().__init__(nombre, vidas, ataque)

    def atacar(self, enemigo) -> None:
        """
        Attack an enemy, dealing damage equal to hero's attack stat.

        Args:
            enemigo: Enemy to attack (must have vidas attribute)
        """
        enemigo.recibir_dano(self.ataque)