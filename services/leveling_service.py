"""
Leveling service for experience and progression calculations.
Follows Single Responsibility Principle - only handles leveling logic.
"""

from typing import Dict, Tuple
from models.hero import Hero


class LevelingService:
    """
    Service responsible for experience calculations and level progression.
    """

    # XP requirements for each level (cumulative)
    XP_REQUIREMENTS = {
        1: 0,
        2: 100,
        3: 250,
        4: 450,
        5: 700,
        6: 1000,
        7: 1350,
        8: 1750,
        9: 2200,
        10: 2700,
        # Add more levels as needed
    }

    # Stat growth per level
    STAT_GROWTH = {
        "health": 10,
        "attack": 2,
        "defense": 1
    }

    @staticmethod
    def calculate_experience_for_level(level: int) -> int:
        """
        Calculate total experience required for a given level.

        Args:
            level: Target level

        Returns:
            Total experience required
        """
        if level in LevelingService.XP_REQUIREMENTS:
            return LevelingService.XP_REQUIREMENTS[level]

        # Extrapolate for higher levels
        base_xp = LevelingService.XP_REQUIREMENTS[10]
        return base_xp + (level - 10) * 500  # 500 XP per level after 10

    @staticmethod
    def get_experience_to_next_level(current_level: int, current_xp: int) -> int:
        """
        Calculate experience needed to reach next level.

        Args:
            current_level: Current hero level
            current_xp: Current experience points

        Returns:
            Experience needed for next level
        """
        next_level_xp = LevelingService.calculate_experience_for_level(current_level + 1)
        return max(0, next_level_xp - current_xp)

    @staticmethod
    def calculate_level_from_experience(total_xp: int) -> int:
        """
        Calculate level based on total experience.

        Args:
            total_xp: Total experience points

        Returns:
            Current level
        """
        level = 1
        for lvl, xp_required in LevelingService.XP_REQUIREMENTS.items():
            if total_xp >= xp_required:
                level = lvl
            else:
                break

        # Handle levels beyond predefined requirements
        if total_xp > LevelingService.XP_REQUIREMENTS[10]:
            extra_levels = (total_xp - LevelingService.XP_REQUIREMENTS[10]) // 500
            level = 10 + extra_levels + 1  # +1 because we want the level they're at

        return level

    @staticmethod
    def apply_level_up(hero: Hero) -> Dict[str, int]:
        """
        Apply level up bonuses to hero.

        Args:
            hero: Hero to level up

        Returns:
            Dictionary of stat increases
        """
        bonuses = {
            "health": LevelingService.STAT_GROWTH["health"],
            "attack": LevelingService.STAT_GROWTH["attack"],
            "defense": LevelingService.STAT_GROWTH.get("defense", 0)
        }

        # Apply bonuses
        hero.base_health += bonuses["health"]
        hero.base_attack += bonuses["attack"]
        hero.health += bonuses["health"]  # Also heal current HP
        hero.attack += bonuses["attack"]

        # Grant skill point
        hero.skill_points += 1

        return bonuses

    @staticmethod
    def get_experience_reward(enemy_level: int, hero_level: int) -> int:
        """
        Calculate experience reward for defeating an enemy.

        Args:
            enemy_level: Level of defeated enemy
            hero_level: Level of hero

        Returns:
            Experience points rewarded
        """
        base_xp = 25  # Base XP per enemy

        # Level difference multiplier
        level_diff = enemy_level - hero_level
        if level_diff > 0:
            multiplier = 1.5 + (level_diff * 0.2)  # Bonus for higher level enemies
        elif level_diff < 0:
            multiplier = max(0.1, 1.0 + (level_diff * 0.1))  # Reduced XP for lower level enemies
        else:
            multiplier = 1.0

        return int(base_xp * multiplier)

    @staticmethod
    def get_level_progress(hero: Hero) -> Dict[str, any]:
        """
        Get detailed level progress information.

        Args:
            hero: Hero to check progress for

        Returns:
            Dictionary with progress information
        """
        current_level_xp = LevelingService.calculate_experience_for_level(hero.level)
        next_level_xp = LevelingService.calculate_experience_for_level(hero.level + 1)

        progress_xp = hero.experience - current_level_xp
        required_xp = next_level_xp - current_level_xp

        progress_percentage = (progress_xp / required_xp) * 100 if required_xp > 0 else 100

        return {
            "current_level": hero.level,
            "current_xp": hero.experience,
            "xp_for_current_level": current_level_xp,
            "xp_for_next_level": next_level_xp,
            "progress_xp": progress_xp,
            "required_xp": required_xp,
            "progress_percentage": progress_percentage,
            "skill_points": hero.skill_points
        }

    @staticmethod
    def can_level_up(hero: Hero) -> bool:
        """
        Check if hero can level up.

        Args:
            hero: Hero to check

        Returns:
            True if hero can level up, False otherwise
        """
        required_xp = LevelingService.calculate_experience_for_level(hero.level + 1)
        return hero.experience >= required_xp

    @staticmethod
    def process_experience_gain(hero: Hero, xp_gained: int) -> Tuple[bool, int]:
        """
        Process experience gain and handle level ups.

        Args:
            hero: Hero gaining experience
            xp_gained: Experience points gained

        Returns:
            Tuple of (leveled_up, levels_gained)
        """
        initial_level = hero.level
        hero.experience += xp_gained

        levels_gained = 0
        leveled_up = False

        while LevelingService.can_level_up(hero):
            LevelingService.apply_level_up(hero)
            levels_gained += 1
            leveled_up = True

        return leveled_up, levels_gained