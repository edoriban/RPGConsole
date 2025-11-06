"""
Game service following Single Responsibility Principle.
Orchestrates the main game flow and coordinates other services.
"""

import random
from models.hero import Hero
from models.monster import Monster
from data.monsters import get_monster_names, get_monster_stats
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

    def start_game(self) -> None:
        """Start and run the complete game."""
        self.ui.show_welcome()

        hero_name = self.ui.prompt_hero_name()
        hero = Hero(hero_name)

        self.ui.show_hero_stats(hero)
        self._process_path_selection(hero)

        self.ui.show_farewell(hero)

    def _process_path_selection(self, hero: Hero) -> None:
        """
        Handle path selection and subsequent game flow.

        Args:
            hero: Hero character
        """
        self.ui.show_path_menu()
        choice = self.ui.get_path_choice()

        if choice == 1:
            self._process_forest_path()
        elif choice == 2:
            self._process_cave_path(hero)
        else:
            self.ui.show_game_over()

    def _process_forest_path(self) -> None:
        """Handle forest path - safe route."""
        self.ui.show_forest_path()

    def _process_cave_path(self, hero: Hero) -> None:
        """
        Handle cave path - dangerous route with combat.

        Args:
            hero: Hero character
        """
        self.ui.show_cave_entrance()

        monster = self._create_random_monster()
        self.ui.show_monster_appears(monster)

        victory = self.combat_service.start_combat(hero, monster)

        if victory:
            self.ui.show_victory(monster)
        else:
            self.ui.show_defeat(monster)

    def _create_random_monster(self) -> Monster:
        """
        Create a random monster from the catalog.

        Returns:
            Randomly selected monster instance
        """
        names = get_monster_names()
        chosen_name = random.choice(names)
        stats = get_monster_stats(chosen_name)

        return Monster(
            name=chosen_name,
            health=stats["health"],
            attack=stats["attack"]
        )