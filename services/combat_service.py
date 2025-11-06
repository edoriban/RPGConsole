"""
Combat service following Single Responsibility Principle.
Handles all combat-related logic and calculations.
"""

import random
from typing import Tuple, Optional
from models.character import Character
from models.hero import Hero
from models.monster import Monster
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

    def start_combat(self, hero: Hero, monster: Monster) -> bool:
        """
        Execute complete combat sequence.

        Args:
            hero: Hero character
            monster: Monster character

        Returns:
            True if hero wins, False if hero loses
        """
        self.ui.show_combat_start()

        while hero.is_alive() and monster.is_alive():
            self._execute_turn(hero, monster)

        return hero.is_alive()

    def _execute_turn(self, hero: Hero, monster: Monster) -> None:
        """
        Execute a single combat turn with three action choices.

        Args:
            hero: Hero character
            monster: Monster character
        """
        self.ui.show_combat_status(hero, monster)
        self.ui.show_combat_menu()
        self.ui.show_combat_options(hero)

        choice = self.ui.get_combat_choice()

        # Reset defense at start of turn
        hero.reset_defense()

        if choice == 1:
            self._process_hero_attack(hero, monster)
        elif choice == 2:
            self._process_hero_defense(hero)
        elif choice == 3:
            self._process_item_usage(hero)
        elif choice == 4:
            self._process_skill_usage(hero, monster)
        else:
            self.ui.show_invalid_choice()

        # Monster turn
        if monster.is_alive():
            self._process_monster_turn(hero, monster)

    def _process_hero_attack(self, hero: Hero, monster: Monster) -> None:
        """
        Process hero attack action.

        Args:
            hero: Hero character
            monster: Monster character
        """
        # Call the hero's attack method directly
        hero.attack(monster)
        self.ui.show_successful_attack(hero, monster)

    def _process_hero_defense(self, hero: Hero) -> None:
        """
        Process hero defense action.

        Args:
            hero: Hero character
        """
        hero.defend()
        self.ui.show_defense_activated()

    def _process_item_usage(self, hero: Hero) -> None:
        """
        Process item usage action.

        Args:
            hero: Hero character
        """
        consumables = hero.inventory.get_consumables()
        if not consumables:
            print("You have no items to use!")
            return

        print("Available items:")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item}")

        try:
            choice = int(input("Choose item to use (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(consumables):
                selected_item = consumables[choice - 1]
                if hero.use_item(selected_item.name):
                    print(f"Used {selected_item.name}!")
                else:
                    print(f"Could not use {selected_item.name}!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

    def _process_skill_usage(self, hero, monster) -> None:
        """
        Process skill usage action.

        Args:
            hero: Hero character
            monster: Monster character
        """
        # For now, placeholder - skills system not fully integrated
        print("Skills system not yet implemented in combat!")
        print("Use regular attack instead.")

    def _process_monster_turn(self, hero: Hero, monster: Monster) -> None:
        """
        Process monster turn.

        Args:
            hero: Hero character
            monster: Monster character
        """
        self.ui.show_monster_attack(monster)

        if hero.is_defending:
            damage = monster.attack // 2
            hero.take_damage(damage)
            self.ui.show_successful_defense(damage)
            hero.reset_defense()
        else:
            hero.take_damage(monster.attack)
            self.ui.show_full_damage(monster, monster.attack)