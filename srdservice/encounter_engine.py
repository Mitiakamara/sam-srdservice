"""
Encounter Engine v1.0
---------------------
Generador de encuentros equilibrados para S.A.M.
Basado en el Dungeon Master's Guide (XP thresholds + CR system)
y datos de monstruos del SRD 5.2.1 Simplificado.
"""

import random
from typing import List, Dict, Any

# Tabla XP por nivel y dificultad (SRD / DMG)
XP_THRESHOLDS = {
    1: {"easy": 25, "medium": 50, "hard": 75, "deadly": 100},
    2: {"easy": 50, "medium": 100, "hard": 150, "deadly": 200},
    3: {"easy": 75, "medium": 150, "hard": 225, "deadly": 400},
    4: {"easy": 125, "medium": 250, "hard": 375, "deadly": 500},
    5: {"easy": 250, "medium": 500, "hard": 750, "deadly": 1100},
    6: {"easy": 300, "medium": 600, "hard": 900, "deadly": 1400},
    7: {"easy": 350, "medium": 750, "hard": 1100, "deadly": 1700},
    8: {"easy": 450, "medium": 900, "hard": 1400, "deadly": 2100},
    9: {"easy": 550, "medium": 1100, "hard": 1600, "deadly": 2400},
    10: {"easy": 600, "medium": 1200, "hard": 1900, "deadly": 2800}
}

def _get_multiplier(n: int) -> float:
    """Multiplicador de dificultad según cantidad de enemigos."""
    if n == 1: return 1.0
    if n == 2: return 1.5
    if 3 <= n <= 6: return 2.0
    if 7 <= n <= 10: return 2.5
    if 11 <= n <= 14: return 3.0
    return 4.0

def generate_encounter(party_levels: List[int], monsters_data: Dict[str, Any], difficulty: str = "medium") -> Dict[str, Any]:
    """Genera un encuentro de combate equilibrado según el nivel del grupo."""
    if not party_levels:
        raise ValueError("Debe indicarse al menos un nivel de personaje.")
    if difficulty not in ["easy", "medium", "hard", "deadly"]:
        difficulty = "medium"

    avg_lvl = sum(party_levels) / len(party_levels)
    n_players = len(party_levels)

    # 1️⃣ Calcular XP objetivo
    lvl_key = max(1, min(10, round(avg_lvl)))
    xp_target = XP_THRESHOLDS[lvl_key][difficulty] * n_players

    # 2️⃣ Seleccionar monstruos
    names = list(monsters_data.keys())
    selected = []
    total_xp = 0
    attempts = 0

    while total_xp < xp_target and attempts < 100:
        m_name = random.choice(names)
        m_data = monsters_data[m_name]
        total_xp += m_data.get("xp", 0)
        selected.append({"name": m_name, **m_data})
        attempts += 1

    # 3️⃣ Ajustar dificultad
    multiplier = _get_multiplier(len(selected))
    adjusted_xp = int(total_xp * multiplier)

    return {
        "party_avg_lvl": round(avg_lvl, 2),
        "difficulty": difficulty,
        "xp_target": xp_target,
        "xp_total": adjusted_xp,
        "monsters": selected
    }

if __name__ == "__main__":
    # Prueba rápida local
    sample_monsters = {
        "Goblin": {"cr": 0.25, "xp": 50, "hp": 7, "ac": 15},
        "Wolf": {"cr": 0.25, "xp": 50, "hp": 11, "ac": 13},
        "Bandit": {"cr": 0.125, "xp": 25, "hp": 11, "ac": 12}
    }
    test = generate_encounter([3, 3, 3], sample_monsters, "medium")
    print(test)
