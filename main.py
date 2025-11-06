"""
RPGConsole - Main entry point
Educational RPG game demonstrating clean code and SOLID principles.
"""

from ui.console_ui import ConsoleUI
from services.combat_service import CombatService
from services.game_service import GameService


def main():
    """Application entry point."""
    # Initialize services following Dependency Inversion Principle
    ui = ConsoleUI()
    combat_service = CombatService(ui)
    game_service = GameService(ui, combat_service)

    # Start the game
    game_service.start_game()


if __name__ == "__main__":
    main()