"""
Monster data catalog.
Follows Single Responsibility Principle - only contains monster definitions.
"""

from typing import Dict, List

# Monster catalog following Open/Closed Principle - can be extended without modification
CATALOGO_MONSTRUOS: Dict[str, Dict[str, int]] = {
    "Goblin": {"vidas": 60, "ataque": 12},
    "Ogro": {"vidas": 60, "ataque": 12},
    "Orco": {"vidas": 60, "ataque": 12},
    "Slime": {"vidas": 60, "ataque": 12}
}


def obtener_nombres_monstruos() -> List[str]:
    """
    Get list of all available monster names.

    Returns:
        List of monster names
    """
    return list(CATALOGO_MONSTRUOS.keys())


def obtener_stats_monstruo(nombre: str) -> Dict[str, int]:
    """
    Get monster stats by name.

    Args:
        nombre: Monster name

    Returns:
        Dictionary with monster stats

    Raises:
        KeyError: If monster name doesn't exist
    """
    return CATALOGO_MONSTRUOS[nombre].copy()