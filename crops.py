#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crop data and constants for Palia Garden Optimizer
"""

# Crop definitions with effects and sizes
CROPS = {
    "Apple": {"effect": "harvest", "size": (3, 3)},           # Apple Tree 3×3 - FIXED: harvest boost
    "Butterfly Bean": {"effect": "harvest", "size": (2, 2)},  # 2×2
    "Blueberry": {"effect": "harvest", "size": (2, 2)},       # 2×2 - FIXED: harvest boost
    "Bok Choy": {"effect": "weed", "size": (1, 1)},
    "Carrot": {"effect": "weed", "size": (1, 1)},
    "Corn": {"effect": "harvest", "size": (1, 1)},
    "Cotton": {"effect": "quality", "size": (1, 1)},
    "Lettuce": {"effect": None, "size": (1, 1)},
    "Napa Cabbage": {"effect": "water", "size": (1, 1)},
    "Onion": {"effect": "weed", "size": (1, 1)},
    "Potato": {"effect": "water", "size": (1, 1)},
    "Rice": {"effect": "harvest", "size": (1, 1)},
    "Rockhopper Pumpkin": {"effect": "quality", "size": (2, 2)},
    "Spicy Pepper": {"effect": "quality", "size": (2, 2)},
    "Tomato": {"effect": "water", "size": (1, 1)},
    "Wheat": {"effect": "harvest", "size": (1, 1)},
}

# Colors per effect
COLOR = {
    name: {
        "harvest": "#f1c40f",
        "water": "#3498db",
        "quality": "#9b59b6",
        "weed": "#27ae60",
        "growth": "#2980b9",
        None: "#7f8c8d",
    }[meta["effect"]]
    for name, meta in CROPS.items()
}

# Scoring weights
BONUS_WEIGHT = {"harvest": 1.0, "quality": 0.8, "growth": 0.8, "water": 0.6, "weed": 0.3}
PREFERRED_WEIGHT = 0.5
SAME_SPECIES_ADJ_PENALTY = 0.25
