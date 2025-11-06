"""
Console UI service following Single Responsibility Principle.
Handles all user interface interactions and display logic.
"""

from colorama import init, Fore, Style
from typing import Optional

# Initialize colorama
init(autoreset=True)


class ConsoleUI:
    """
    Console User Interface service.
    Responsible only for displaying information and getting user input.
    """

    @staticmethod
    def show_welcome() -> None:
        """Display welcome message."""
        print(Fore.YELLOW + "Welcome to the caves of activity 4!")

    @staticmethod
    def prompt_hero_name() -> str:
        """
        Prompt user for hero name.

        Returns:
            Hero name entered by user
        """
        return input(Fore.YELLOW + "Enter your hero's name: ")

    @staticmethod
    def show_hero_stats(hero) -> None:
        """
        Display detailed hero statistics.

        Args:
            hero: Hero object with all attributes
        """
        print("==================================================")
        print(f"HERO STATUS: {hero.name}")
        print("==================================================")
        print(f"Level: {hero.level} (XP: {hero.experience}/{hero.experience_to_next})")
        print(f"Health: {hero.health}/{hero.base_health + (hero.level - 1) * 10}")
        print(f"Attack: {hero.get_total_attack()} (Base: {hero.base_attack})")
        print(f"Skill Points: {hero.skill_points}")
        print(f"Gold: {hero.inventory.gold}")
        print("--------------------------------------------------")
        print("Equipment:")
        equipped_items = [item for item in hero.inventory.get_all_items()
                         if hasattr(item, 'equipped') and item.equipped]
        if equipped_items:
            for item in equipped_items:
                print(f"  - {item}")
        else:
            print("  - None")
        print("--------------------------------------------------")
        print(f"Inventory: {hero.inventory.get_total_slots_used()}/{hero.inventory.max_slots}")
        print("==================================================")

    @staticmethod
    def show_path_menu() -> None:
        """Display path selection menu."""
        print("You arrive at a fork in the road.")
        print("One path leads to the peaceful forest, the other to a dark cave.")
        print(" ")
        print(Fore.YELLOW + "1. Go through the forest (Safe Route).")
        print(Fore.YELLOW + "2. Enter the cave (Dangerous Route).")

    @staticmethod
    def get_path_choice() -> int:
        """
        Get path choice from user.

        Returns:
            Integer choice (1 or 2)
        """
        return int(input())

    @staticmethod
    def show_forest_path() -> None:
        """Display forest path message."""
        print("You decide to take the forest path.")
        print("It's a pleasant walk and you arrive at the village without incident.")

    @staticmethod
    def show_cave_entrance() -> None:
        """Display cave entrance message."""
        print("Bravely, you enter the dark cave...")

    @staticmethod
    def show_monster_appears(monster) -> None:
        """
        Display monster appearance message.

        Args:
            monster: Monster object with name attribute
        """
        print(f"A wild {monster.name} appears!")

    @staticmethod
    def show_combat_start() -> None:
        """Display combat start message."""
        print(Fore.YELLOW + "COMBAT BEGINS!")

    @staticmethod
    def show_combat_status(hero, monster) -> None:
        """
        Display current combat status.

        Args:
            hero: Hero object
            monster: Monster object
        """
        print("--- NEW TURN ---")
        print(f"{hero.name}'s Health: {hero.health}")
        print(f"{monster.name}'s Health: {monster.health}")
        print(" ")

    @staticmethod
    def show_combat_menu() -> None:
        """Display combat action menu."""
        print(Fore.YELLOW + "What will you do?")

    @staticmethod
    def show_combat_options(hero) -> None:
        """
        Display combat options.

        Args:
            hero: Hero object with attack attribute
        """
        print(Fore.YELLOW + f"1. Attack ({hero.get_total_attack()} damage)")
        print(Fore.YELLOW + "2. Defend (reduces next hit by half)")
        print(Fore.YELLOW + "3. Use Item")
        print(Fore.YELLOW + "4. Use Skill")

    @staticmethod
    def get_combat_choice() -> int:
        """
        Get combat choice from user.

        Returns:
            Integer choice (1 or 2)
        """
        return int(input())

    @staticmethod
    def show_successful_attack(attacker, defender) -> None:
        """
        Display successful attack message.

        Args:
            attacker: Attacking character
            defender: Defending character
        """
        print(Fore.GREEN + f"You attack the {defender.name} with all your strength!")
        print(Fore.GREEN + f"You deal {attacker.attack} damage.")

    @staticmethod
    def show_defense_activated() -> None:
        """Display defense activation message."""
        print(Fore.BLUE + "You prepare for the impact, raising your guard.")

    @staticmethod
    def show_monster_attack(monster) -> None:
        """
        Display monster attack message.

        Args:
            monster: Monster object
        """
        print(f"The {monster.name} counterattacks...")

    @staticmethod
    def show_successful_defense(damage: int) -> None:
        """
        Display successful defense message.

        Args:
            damage: Damage received after defense
        """
        print(Fore.BLUE + "You block most of the blow!")
        print(Fore.RED + f"You only take {damage} damage.")

    @staticmethod
    def show_full_damage(monster, damage: int) -> None:
        """
        Display full damage message.

        Args:
            monster: Monster object
            damage: Damage received
        """
        print(Fore.RED + "You take the hit directly!")
        print(Fore.RED + f"You lose {damage} health.")

    @staticmethod
    def show_victory(monster) -> None:
        """
        Display victory message.

        Args:
            monster: Defeated monster object
        """
        print(Fore.GREEN + f"VICTORY! You have defeated the {monster.name}.")
        print(Fore.GREEN + "You find a Python Manual!")
        print(Fore.GREEN + "Your adventure continues...")

    @staticmethod
    def show_defeat(monster) -> None:
        """
        Display defeat message.

        Args:
            monster: Monster that defeated the hero
        """
        print(Fore.RED + f"You have been defeated by the {monster.name}... Game over.")

    @staticmethod
    def show_invalid_choice() -> None:
        """Display invalid choice message."""
        print("Invalid choice, turn lost.")

    @staticmethod
    def show_game_over() -> None:
        """Display game over message."""
        print("You were paralyzed by indecision and a rabbit robbed you.")
        print("Game over.")

    @staticmethod
    def show_farewell(hero) -> None:
        """
        Display farewell message.

        Args:
            hero: Hero object
        """
        print("------------------------------------------------")
        print(f"End of demo. Thanks for playing, {hero.name}.")