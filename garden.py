#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Garden logic and optimization algorithms for Palia Garden Optimizer
"""

import random
from collections import Counter
from crops import CROPS, BONUS_WEIGHT, PREFERRED_WEIGHT, SAME_SPECIES_ADJ_PENALTY

def ortho_neighbors(r, c, rows, cols):
    """Get orthogonal neighbors of a cell"""
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

class Garden:
    """Garden grid management class"""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]  # placement ids
        self.placements = {}  # pid -> {name,r,c,w,h}
        self.next_id = 1

    def clear(self):
        """Clear all plants from the garden"""
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.placements.clear()
        self.next_id = 1

    def can_place(self, name, top_r, top_c):
        """Check if a plant can be placed at given position"""
        w, h = CROPS[name]["size"]
        if top_r < 0 or top_c < 0 or top_r + h > self.rows or top_c + w > self.cols:
            return False
        for r in range(top_r, top_r + h):
            for c in range(top_c, top_c + w):
                if self.grid[r][c] is not None:
                    return False
        return True

    def place(self, name, top_r, top_c):
        """Place a plant at given position"""
        if not self.can_place(name, top_r, top_c):
            return None
        pid = self.next_id; self.next_id += 1
        w, h = CROPS[name]["size"]
        self.placements[pid] = {"name": name, "r": top_r, "c": top_c, "w": w, "h": h}
        for r in range(top_r, top_r + h):
            for c in range(top_c, top_c + w):
                self.grid[r][c] = pid
        return pid

    def remove(self, pid):
        """Remove a plant by placement ID"""
        if pid not in self.placements:
            return
        meta = self.placements.pop(pid)
        for r in range(meta["r"], meta["r"] + meta["h"]):
            for c in range(meta["c"], meta["c"] + meta["w"]):
                self.grid[r][c] = None

    def move(self, pid, new_r, new_c):
        """Move a plant to a new position"""
        if pid not in self.placements:
            return False
        meta = self.placements[pid]
        w, h = meta["w"], meta["h"]
        # remove
        for r in range(meta["r"], meta["r"] + h):
            for c in range(meta["c"], meta["c"] + w):
                self.grid[r][c] = None
        ok = True
        if new_r < 0 or new_c < 0 or new_r + h > self.rows or new_c + w > self.cols:
            ok = False
        else:
            for r in range(new_r, new_r + h):
                for c in range(new_c, new_c + w):
                    if self.grid[r][c] is not None:
                        ok = False; break
                if not ok: break
        if not ok:
            # restore
            for r in range(meta["r"], meta["r"] + h):
                for c in range(meta["c"], meta["c"] + w):
                    self.grid[r][c] = pid
            return False
        meta["r"], meta["c"] = new_r, new_c
        for r in range(new_r, new_r + h):
            for c in range(new_c, new_c + w):
                self.grid[r][c] = pid
        return True

    def clone(self):
        """Create a deep copy of the garden"""
        g = Garden(self.rows, self.cols)
        g.grid = [row[:] for row in self.grid]
        g.placements = {pid: dict(meta) for pid, meta in self.placements.items()}
        g.next_id = self.next_id
        return g

def score_garden_optimized(garden, preferred_name, optimization_mode="balanced"):
    """Enhanced scoring system with different optimization modes"""
    total = 0.0
    bonus_counts = Counter()
    same_species_adjs = 0
    pref_count = 0
    rows, cols = garden.rows, garden.cols
    
    # Define weight multipliers based on optimization mode
    mode_weights = {
        "balanced": {"harvest": 1.0, "quality": 0.8, "growth": 0.8, "water": 0.6, "weed": 0.3},
        "low_maintenance": {"harvest": 0.5, "quality": 0.3, "growth": 0.3, "water": 2.0, "weed": 2.0},
        "max_harvest": {"harvest": 2.0, "quality": 0.5, "growth": 1.0, "water": 0.3, "weed": 0.3},
        "max_quality": {"harvest": 0.8, "quality": 2.0, "growth": 1.0, "water": 0.5, "weed": 0.3}
    }
    
    weights = mode_weights.get(optimization_mode, mode_weights["balanced"])
    
    for pid, meta in garden.placements.items():
        name = meta["name"]
        if name == preferred_name:
            # Boost preferred plant score based on mode
            multiplier = 2.0 if optimization_mode == "low_maintenance" and CROPS[name]["effect"] in ["water", "weed"] else 1.0
            total += PREFERRED_WEIGHT * multiplier
            pref_count += 1
        for r in range(meta["r"], meta["r"] + meta["h"]):
            for c in range(meta["c"], meta["c"] + meta["w"]):
                got_effects = set()
                for nr, nc in ortho_neighbors(r, c, rows, cols):
                    n_pid = garden.grid[nr][nc]
                    if n_pid is None or n_pid == pid:
                        continue
                    n_name = garden.placements[n_pid]["name"]
                    if n_name == name:
                        same_species_adjs += 1
                        total -= SAME_SPECIES_ADJ_PENALTY
                        continue
                    eff = CROPS[n_name]["effect"]
                    if eff:
                        got_effects.add(eff)
                for eff in got_effects:
                    total += weights.get(eff, 0.0)
                    bonus_counts[eff] += 1

    metrics = {
        "total_score": round(total, 3),
        "bonus_counts": dict(bonus_counts),
        "same_species_adj": same_species_adjs,
        "preferred_count": pref_count,
        "optimization_mode": optimization_mode
    }
    return total, metrics

def greedy_fill_optimized(garden, inventory, preferred_name, optimization_mode="balanced"):
    """Enhanced greedy fill with optimization mode priority"""
    to_place = []
    for name, cnt in inventory.items():
        for _ in range(cnt):
            to_place.append(name)
    
    random.shuffle(to_place)
    
    # Sort based on optimization mode
    def get_priority(name):
        effect = CROPS[name]["effect"]
        size_priority = CROPS[name]["size"][0] * CROPS[name]["size"][1]
        
        if optimization_mode == "low_maintenance":
            # Prioritize water and weed effects
            effect_priority = 3 if effect in ["water", "weed"] else 1
        elif optimization_mode == "max_harvest":
            effect_priority = 3 if effect == "harvest" else 1
        elif optimization_mode == "max_quality":
            effect_priority = 3 if effect == "quality" else 1
        else:  # balanced
            effect_priority = 2 if effect in ["harvest", "quality"] else 1
        
        preferred_bonus = 2 if name == preferred_name else 1
        
        return (preferred_bonus, effect_priority, size_priority)
    
    to_place.sort(key=get_priority, reverse=True)
    
    for name in to_place:
        placed = False
        for r in range(garden.rows):
            for c in range(garden.cols):
                if garden.can_place(name, r, c):
                    garden.place(name, r, c)
                    placed = True; break
            if placed: break
    return garden

def local_search_optimized(garden, preferred_name, optimization_mode="balanced", iterations=3000):
    """Enhanced local search with optimization mode"""
    best = garden.clone()
    best_score, _ = score_garden_optimized(best, preferred_name, optimization_mode)
    pids = list(best.placements.keys())
    if not pids:
        return best, best_score
    for _ in range(iterations):
        pid = random.choice(pids)
        meta = best.placements[pid]
        nr = random.randrange(0, best.rows - meta["h"] + 1)
        nc = random.randrange(0, best.cols - meta["w"] + 1)
        cand = best.clone()
        moved = cand.move(pid, nr, nc)
        if not moved: continue
        cand_score, _ = score_garden_optimized(cand, preferred_name, optimization_mode)
        if cand_score >= best_score:
            best, best_score = cand, cand_score
            pids = list(best.placements.keys())
    return best, best_score

# Legacy compatibility functions
def greedy_fill(garden, inventory, preferred_name):
    """Legacy greedy fill function"""
    to_place = []
    for name, cnt in inventory.items():
        for _ in range(cnt):
            to_place.append(name)
    random.shuffle(to_place)
    to_place.sort(key=lambda nm: (nm != preferred_name, -CROPS[nm]["size"][0]*CROPS[nm]["size"][1]))
    for name in to_place:
        placed = False
        for r in range(garden.rows):
            for c in range(garden.cols):
                if garden.can_place(name, r, c):
                    garden.place(name, r, c)
                    placed = True; break
            if placed: break
    return garden

def local_search(garden, preferred_name, iterations=3000):
    """Legacy local search function"""
    best = garden.clone()
    best_score, _ = score_garden_optimized(best, preferred_name, "balanced")
    pids = list(best.placements.keys())
    if not pids:
        return best, best_score
    for _ in range(iterations):
        pid = random.choice(pids)
        meta = best.placements[pid]
        nr = random.randrange(0, best.rows - meta["h"] + 1)
        nc = random.randrange(0, best.cols - meta["w"] + 1)
        cand = best.clone()
        moved = cand.move(pid, nr, nc)
        if not moved: continue
        cand_score, _ = score_garden_optimized(cand, preferred_name, "balanced")
        if cand_score >= best_score:
            best, best_score = cand, cand_score
            pids = list(best.placements.keys())
    return best, best_score
