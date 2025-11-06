"""
Game service following Single Responsibility Principle.
Orchestrates the main game flow and coordinates other services.
"""

import random
from models.hero import Hero
from models.monster import Monster
from models.world.zone import create_forest, create_cave, create_town
from data.monsters import get_monster_names, get_monster_stats
from services.combat_service import CombatService
from services.game_state_service import GameStateService
from ui.console_ui import ConsoleUI


class GameService:
    """
    Main game service that orchestrates the entire game flow.
    Follows Single Responsibility Principle and Dependency Inversion.
    """

    def __init__(self, ui: ConsoleUI, combat_service: CombatService, game_state_service: GameStateService):
        """
        Initialize game service with dependencies.

        Args:
            ui: Console UI service
            combat_service: Combat logic service
            game_state_service: Game state persistence service
        """
        self.ui = ui
        self.combat_service = combat_service
        self.game_state_service = game_state_service
        self.current_zone = None
        self.hero = None

    def start_game(self) -> None:
        """Start and run the complete game."""
        self.ui.show_welcome()

        # Check for existing saves
        saves = self.game_state_service.list_save_files()
        if any(save["exists"] for save in saves.values()):
            if self._ask_load_game():
                if not self._load_game():
                    # If load fails, start new game
                    self._start_new_game()
            else:
                self._start_new_game()
        else:
            self._start_new_game()

        # Main game loop
        self._main_game_loop()

    def _start_new_game(self) -> None:
        """Initialize a new game."""
        hero_name = self.ui.prompt_hero_name()
        self.hero = Hero(hero_name)
        self.current_zone = create_forest()  # Start in forest
        self.current_zone.mark_discovered()
        self.current_zone.mark_visited()

        self.ui.show_hero_stats(self.hero)

    def _ask_load_game(self) -> bool:
        """Ask player if they want to load a saved game."""
        print("Save files found. Would you like to load a game? (y/n)")
        response = input().lower().strip()
        return response in ['y', 'yes']

    def _load_game(self) -> bool:
        """Load a saved game."""
        saves = self.game_state_service.list_save_files()

        print("Available save slots:")
        for slot, info in saves.items():
            if info["exists"]:
                status = f"Level {info.get('level', '?')} {info.get('hero_name', 'Unknown')} in {info.get('zone', 'Unknown')}"
                print(f"{slot}. {status}")
            else:
                print(f"{slot}. (Empty)")

        try:
            slot = int(input("Choose save slot (1-3): "))
            if 1 <= slot <= 3 and saves[slot]["exists"]:
                save_data = self.game_state_service.load_game(slot)
                if save_data:
                    self.hero, self.current_zone = self.game_state_service.reconstruct_game_state(save_data)
                    return True
        except (ValueError, KeyError):
            pass

        print("Failed to load save file.")
        return False

    def _main_game_loop(self) -> None:
        """Main game loop handling zone navigation and actions."""
        while True:
            self._show_current_location()
            action = self._get_player_action()

            if action == "explore":
                self._handle_exploration()
            elif action == "inventory":
                self._show_inventory()
            elif action == "stats":
                self.ui.show_hero_stats(self.hero)
            elif action == "save":
                self._save_game()
            elif action == "quit":
                if self._confirm_quit():
                    break
            elif action == "travel":
                self._handle_travel()
            else:
                print("Invalid action.")

            # Auto-save after each action
            self.game_state_service.auto_save(self.hero, self.current_zone)

    def _show_current_location(self) -> None:
        """Display current zone information."""
        print(f"\n=== {self.current_zone.name} ===")
        print(self.current_zone.description)
        print(f"Danger Level: {self.current_zone.danger_level}")

    def _get_player_action(self) -> str:
        """Get player action choice."""
        actions = ["explore", "inventory", "stats", "save", "travel", "quit"]

        print("\nAvailable actions:")
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action.title()}")

        try:
            choice = int(input("Choose action: "))
            if 1 <= choice <= len(actions):
                return actions[choice - 1]
        except ValueError:
            pass

        return "invalid"

    def _handle_exploration(self) -> None:
        """Handle zone exploration."""
        print(f"You explore {self.current_zone.name}...")
        print(self.current_zone.explore())

        # Check for random encounter
        monster = self.current_zone.generate_random_encounter()
        if monster:
            self.ui.show_monster_appears(monster)
            victory = self.combat_service.start_combat(self.hero, monster)

            if victory:
                self.ui.show_victory(monster)
                # Award experience
                from services.leveling_service import LevelingService
                xp_reward = LevelingService.get_experience_reward(1, self.hero.level)
                leveled_up, levels_gained = LevelingService.process_experience_gain(self.hero, xp_reward)
                print(f"Gained {xp_reward} experience points!")
                if leveled_up:
                    print(f"You gained {levels_gained} level(s)!")
            else:
                self.ui.show_defeat(monster)
        else:
            print("You find nothing dangerous in this area.")

    def _show_inventory(self) -> None:
        """Display hero inventory."""
        print("\n" + "="*50)
        print("INVENTORY")
        print("="*50)
        print(self.hero.get_inventory_summary())

        # Show consumable options
        consumables = self.hero.inventory.get_consumables()
        if consumables:
            print("\nConsumables:")
            for i, item in enumerate(consumables, 1):
                print(f"{i}. {item}")

            print("0. Back")
            try:
                choice = int(input("Use item (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(consumables):
                    selected_item = consumables[choice - 1]
                    if self.hero.use_item(selected_item.name):
                        print(f"Used {selected_item.name}!")
                    else:
                        print(f"Could not use {selected_item.name}!")
            except ValueError:
                print("Invalid choice.")

    def _save_game(self) -> None:
        """Handle game saving."""
        print("Choose save slot (1-3):")
        try:
            slot = int(input())
            if 1 <= slot <= 3:
                if self.game_state_service.save_game(self.hero, self.current_zone, slot):
                    print("Game saved successfully!")
                else:
                    print("Failed to save game.")
            else:
                print("Invalid slot number.")
        except ValueError:
            print("Invalid input.")

    def _confirm_quit(self) -> bool:
        """Confirm game quit."""
        response = input("Are you sure you want to quit? (y/n): ").lower().strip()
        return response in ['y', 'yes']

    def _handle_travel(self) -> None:
        """Handle zone travel."""
        zones = [create_forest(), create_cave(), create_town()]

        print("Available destinations:")
        for i, zone in enumerate(zones, 1):
            status = "(Current)" if zone.name == self.current_zone.name else ""
            print(f"{i}. {zone.name} {status}")

        try:
            choice = int(input("Choose destination: "))
            if 1 <= choice <= len(zones):
                selected_zone = zones[choice - 1]
                if selected_zone.name != self.current_zone.name:
                    self.current_zone = selected_zone
                    self.current_zone.mark_discovered()
                    self.current_zone.mark_visited()
                    print(f"You travel to {self.current_zone.name}.")
                else:
                    print("You are already in that zone.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

    def _process_path_selection(self, hero: Hero) -> None:
        """
        Legacy method for backward compatibility.
        Handle path selection and subsequent game flow.

        Args:
            hero: Hero character
        """
        self.ui.show_path_menu()
        choice = self.ui.get_path_choice()

        if choice == 1:
            self.current_zone = create_forest()
            self._handle_exploration()
        elif choice == 2:
            self.current_zone = create_cave()
            self._handle_exploration()
        else:
            self.ui.show_game_over()