"""
Game state management service.
Handles saving and loading game progress.
"""

import json
import os
from typing import Dict, Any, Optional
from models.hero import Hero
from models.world.zone import Zone, SafeZone, CombatZone


class GameStateService:
    """
    Service for managing game state persistence.
    Handles saving and loading game progress to/from files.
    """

    SAVE_DIR = "saves"
    SAVE_EXTENSION = ".json"

    def __init__(self):
        """Initialize the game state service."""
        self.ensure_save_directory()

    def ensure_save_directory(self) -> None:
        """Ensure the save directory exists."""
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)

    def save_game(self, hero: Hero, current_zone: Zone, slot: int = 1) -> bool:
        """
        Save the current game state.

        Args:
            hero: Current hero state
            current_zone: Current zone
            slot: Save slot number (1-3)

        Returns:
            True if save was successful, False otherwise
        """
        try:
            save_data = {
                "hero": hero.to_dict(),
                "current_zone": current_zone.to_dict(),
                "game_version": "1.0.0",
                "save_slot": slot
            }

            filename = self._get_save_filename(slot)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"Game saved to slot {slot}!")
            return True

        except Exception as e:
            print(f"Failed to save game: {e}")
            return False

    def load_game(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Load a saved game state.

        Args:
            slot: Save slot number (1-3)

        Returns:
            Dictionary with loaded game data, or None if load failed
        """
        try:
            filename = self._get_save_filename(slot)
            if not os.path.exists(filename):
                print(f"No save file found in slot {slot}")
                return None

            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Validate save data
            if not self._validate_save_data(save_data):
                print("Save file is corrupted or incompatible")
                return None

            print(f"Game loaded from slot {slot}!")
            return save_data

        except Exception as e:
            print(f"Failed to load game: {e}")
            return None

    def reconstruct_game_state(self, save_data: Dict[str, Any]) -> tuple[Hero, Zone]:
        """
        Reconstruct hero and zone objects from save data.

        Args:
            save_data: Loaded save data

        Returns:
            Tuple of (hero, current_zone)
        """
        try:
            # Reconstruct hero
            hero_data = save_data["hero"]
            hero = Hero.from_dict(hero_data)

            # Reconstruct current zone
            zone_data = save_data["current_zone"]
            zone_type = zone_data.get("type", "CombatZone")

            if zone_type == "SafeZone":
                current_zone = SafeZone.from_dict(zone_data)
            else:
                current_zone = CombatZone.from_dict(zone_data)

            return hero, current_zone

        except Exception as e:
            print(f"Failed to reconstruct game state: {e}")
            raise

    def list_save_files(self) -> Dict[int, Dict[str, Any]]:
        """
        List all available save files with basic info.

        Returns:
            Dictionary mapping slot numbers to save info
        """
        saves = {}
        for slot in range(1, 4):  # Slots 1-3
            filename = self._get_save_filename(slot)
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    hero_data = data.get("hero", {})
                    saves[slot] = {
                        "hero_name": hero_data.get("name", "Unknown"),
                        "level": hero_data.get("level", 1),
                        "zone": data.get("current_zone", {}).get("name", "Unknown"),
                        "exists": True
                    }
                except:
                    saves[slot] = {"exists": False, "error": True}
            else:
                saves[slot] = {"exists": False}

        return saves

    def delete_save(self, slot: int) -> bool:
        """
        Delete a save file.

        Args:
            slot: Save slot number

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            filename = self._get_save_filename(slot)
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Save slot {slot} deleted!")
                return True
            else:
                print(f"No save file found in slot {slot}")
                return False
        except Exception as e:
            print(f"Failed to delete save: {e}")
            return False

    def _get_save_filename(self, slot: int) -> str:
        """
        Get the filename for a save slot.

        Args:
            slot: Save slot number

        Returns:
            Full path to save file
        """
        return os.path.join(self.SAVE_DIR, f"save_slot_{slot}{self.SAVE_EXTENSION}")

    def _validate_save_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate that save data has required fields.

        Args:
            data: Save data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["hero", "current_zone", "game_version"]
        return all(field in data for field in required_fields)

    def auto_save(self, hero: Hero, current_zone: Zone) -> None:
        """
        Perform an automatic save to slot 0 (auto-save slot).

        Args:
            hero: Current hero state
            current_zone: Current zone
        """
        try:
            self.save_game(hero, current_zone, slot=0)
        except:
            # Auto-save failures shouldn't interrupt gameplay
            pass

    def quick_load(self) -> Optional[tuple[Hero, Zone]]:
        """
        Quick load from auto-save slot.

        Returns:
            Tuple of (hero, zone) or None if failed
        """
        save_data = self.load_game(slot=0)
        if save_data:
            try:
                return self.reconstruct_game_state(save_data)
            except:
                return None
        return None