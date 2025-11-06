"""
Character model following SOLID principles.
Single Responsibility: Handle character attributes and basic actions.
Open/Closed: Can be extended through inheritance.
"""

from abc import ABC, abstractmethod


class Personaje(ABC):
    """
    Abstract base class for all characters in the game.
    Follows Single Responsibility Principle by only handling character state.
    """

    def __init__(self, nombre: str, vidas: int, ataque: int):
        """
        Initialize a character with basic attributes.

        Args:
            nombre: Character name
            vidas: Health points
            ataque: Attack damage
        """
        self.nombre = nombre
        self.vidas = vidas
        self.ataque = ataque
        self.esta_defendiendo = False

    @abstractmethod
    def atacar(self, enemigo) -> None:
        """
        Abstract method for attacking an enemy.
        Must be implemented by concrete subclasses.
        """
        pass

    def defender(self) -> None:
        """
        Set defensive stance.
        Follows Open/Closed Principle - can be extended by subclasses.
        """
        self.esta_defendiendo = True

    def recibir_dano(self, dano: int) -> None:
        """
        Apply damage to the character.

        Args:
            dano: Amount of damage to apply
        """
        self.vidas -= dano
        if self.vidas < 0:
            self.vidas = 0

    def esta_vivo(self) -> bool:
        """
        Check if character is still alive.

        Returns:
            True if character has health > 0, False otherwise
        """
        return self.vidas > 0

    def reset_defensa(self) -> None:
        """Reset defensive stance after a turn."""
        self.esta_defendiendo = False