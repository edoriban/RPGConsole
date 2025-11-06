"""
Combat service following Single Responsibility Principle.
Handles all combat-related logic and calculations.
"""

import random
from typing import Tuple, Optional
from models.personaje import Personaje
from models.heroe import Heroe
from models.monstruo import Monstruo
from ui.console_ui import ConsoleUI


class CombatService:
    """
    Service responsible for managing combat mechanics.
    Follows Dependency Inversion Principle by depending on abstractions.
    """

    def __init__(self, ui: ConsoleUI):
        """
        Initialize combat service with UI dependency.

        Args:
            ui: Console UI service for displaying messages
        """
        self.ui = ui

    def iniciar_combate(self, heroe: Heroe, monstruo: Monstruo) -> bool:
        """
        Execute complete combat sequence.

        Args:
            heroe: Hero character
            monstruo: Monster character

        Returns:
            True if hero wins, False if hero loses
        """
        self.ui.mostrar_inicio_combate()

        while heroe.esta_vivo() and monstruo.esta_vivo():
            self._ejecutar_turno(heroe, monstruo)

        return heroe.esta_vivo()

    def _ejecutar_turno(self, heroe: Heroe, monstruo: Monstruo) -> None:
        """
        Execute a single combat turn.

        Args:
            heroe: Hero character
            monstruo: Monster character
        """
        self.ui.mostrar_estado_combate(heroe, monstruo)
        self.ui.mostrar_menu_combate()
        self.ui.mostrar_opciones_combate(heroe)

        decision = self.ui.solicitar_decision_combate()

        # Reset defense at start of turn
        heroe.reset_defensa()

        if decision == 1:
            self._procesar_ataque_heroe(heroe, monstruo)
        elif decision == 2:
            self._procesar_defensa_heroe(heroe)
        else:
            self.ui.mostrar_decision_invalida()

        # Monster turn
        if monstruo.esta_vivo():
            self._procesar_turno_monstruo(heroe, monstruo)

    def _procesar_ataque_heroe(self, heroe: Heroe, monstruo: Monstruo) -> None:
        """
        Process hero attack action.

        Args:
            heroe: Hero character
            monstruo: Monster character
        """
        heroe.atacar(monstruo)
        self.ui.mostrar_ataque_exitoso(heroe, monstruo)

    def _procesar_defensa_heroe(self, heroe: Heroe) -> None:
        """
        Process hero defense action.

        Args:
            heroe: Hero character
        """
        heroe.defender()
        self.ui.mostrar_defensa_activada()

    def _procesar_turno_monstruo(self, heroe: Heroe, monstruo: Monstruo) -> None:
        """
        Process monster turn.

        Args:
            heroe: Hero character
            monstruo: Monster character
        """
        self.ui.mostrar_ataque_monstruo(monstruo)

        if heroe.esta_defendiendo:
            dano = monstruo.ataque // 2
            heroe.recibir_dano(dano)
            self.ui.mostrar_defensa_exitosa(dano)
            heroe.reset_defensa()
        else:
            heroe.recibir_dano(monstruo.ataque)
            self.ui.mostrar_dano_completo(monstruo, monstruo.ataque)