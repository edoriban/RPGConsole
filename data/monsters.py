"""
Monster data catalog.
Follows Single Responsibility Principle - only contains monster definitions.
"""

from typing import Dict, List

# Monster catalog following Open/Closed Principle - can be extended without modification
MONSTER_CATALOG: Dict[str, Dict[str, int]] = {
    "Goblin": {"health": 60, "attack": 12},
    "Ogre": {"health": 60, "attack": 12},
    "Orc": {"health": 60, "attack": 12},
    "Slime": {"health": 60, "attack": 12}
}


def get_monster_names() -> List[str]:
    """
    Get list of all available monster names.

    Returns:
        List of monster names
    """
    return list(MONSTER_CATALOG.keys())


def get_monster_stats(name: str) -> Dict[str, int]:
    """
    Get monster stats by name.

    Args:
        name: Monster name

    Returns:
        Dictionary with monster stats

    Raises:
        KeyError: If monster name doesn't exist
    """
    return MONSTER_CATALOG[name].copy()