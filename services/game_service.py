"""
Game service following Single Responsibility Principle.
Orchestrates the main game flow and coordinates other services.
"""

import random
from models.heroe import Heroe
from models.monstruo import Monstruo
from data.monsters import obtener_nombres_monstruos, obtener_stats_monstruo
from services.combat_service import CombatService
from ui.console_ui import ConsoleUI


class GameService:
    """
    Main game service that orchestrates the entire game flow.
    Follows Single Responsibility Principle and Dependency Inversion.
    """

    def __init__(self, ui: ConsoleUI, combat_service: CombatService):
        """
        Initialize game service with dependencies.

        Args:
            ui: Console UI service
            combat_service: Combat logic service
        """
        self.ui = ui
        self.combat_service = combat_service

    def iniciar_juego(self) -> None:
        """Start and run the complete game."""
        self.ui.mostrar_bienvenida()

        nombre_heroe = self.ui.solicitar_nombre_heroe()
        heroe = Heroe(nombre_heroe)

        self.ui.mostrar_estadisticas_heroe(heroe)
        self._procesar_seleccion_camino(heroe)

        self.ui.mostrar_despedida(heroe)

    def _procesar_seleccion_camino(self, heroe: Heroe) -> None:
        """
        Handle path selection and subsequent game flow.

        Args:
            heroe: Hero character
        """
        self.ui.mostrar_menu_camino()
        decision = self.ui.solicitar_decision_camino()

        if decision == 1:
            self._procesar_camino_bosque()
        elif decision == 2:
            self._procesar_camino_cueva(heroe)
        else:
            self.ui.mostrar_fin_juego()

    def _procesar_camino_bosque(self) -> None:
        """Handle forest path - safe route."""
        self.ui.mostrar_camino_bosque()

    def _procesar_camino_cueva(self, heroe: Heroe) -> None:
        """
        Handle cave path - dangerous route with combat.

        Args:
            heroe: Hero character
        """
        self.ui.mostrar_entrada_cueva()

        monstruo = self._crear_monstruo_aleatorio()
        self.ui.mostrar_monstruo_aparece(monstruo)

        victoria = self.combat_service.iniciar_combate(heroe, monstruo)

        if victoria:
            self.ui.mostrar_victoria(monstruo)
        else:
            self.ui.mostrar_derrota(monstruo)

    def _crear_monstruo_aleatorio(self) -> Monstruo:
        """
        Create a random monster from the catalog.

        Returns:
            Randomly selected monster instance
        """
        nombres = obtener_nombres_monstruos()
        nombre_elegido = random.choice(nombres)
        stats = obtener_stats_monstruo(nombre_elegido)

        return Monstruo(
            nombre=nombre_elegido,
            vidas=stats["vidas"],
            ataque=stats["ataque"]
        )