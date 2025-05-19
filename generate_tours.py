#!/usr/bin/env python3
"""
Generate *diverse* knight's tours on a 7×7 board, always starting at (0,0),
sampling up to MAX_TOURS total by collecting half from each of the two first‐move branches.
"""

import json
import sys
import random

# allow deep recursion for backtracking
sys.setrecursionlimit(10_000_000)

SIZE = 7
KNIGHT_MOVES = [
    (1, 2), (2, 1),
    (-1, 2), (-2, 1),
    (1, -2), (2, -1),
    (-1, -2), (-2, -1)
]

# Global cap (optional)
try:
    GLOBAL_CAP = int(sys.argv[1])
    if GLOBAL_CAP < 1:
        GLOBAL_CAP = None
except:
    GLOBAL_CAP = None  # no limit

# Two valid first moves from (0,0)
FIRST_STEPS = [(1,2), (2,1)]
# shuffle to avoid always exhausting the same branch first
random.shuffle(FIRST_STEPS)

# split cap evenly
per_branch = (GLOBAL_CAP // len(FIRST_STEPS)) if GLOBAL_CAP else None

found = []  # will collect all complete tours

def backtrack(path, visited, local_cap):
    # stop this branch if we've hit its quota
    if local_cap is not None and len(found_branch) >= local_cap:
        return True

    # if full length, record complete tour
    if len(path) == SIZE*SIZE:
        found_branch.append(path.copy())
        return False  # continue searching (unless capped)

    # build Warnsdorff‐ordered candidates
    x0,y0 = path[-1]
    cands = []
    for dx,dy in KNIGHT_MOVES:
        nx,ny = x0+dx, y0+dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx,ny) not in visited:
            # count onward moves
            deg = 0
            for ddx,ddy in KNIGHT_MOVES:
                ax,ay = nx+ddx, ny+ddy
                if 0 <= ax < SIZE and 0 <= ay < SIZE and (ax,ay) not in visited:
                    deg += 1
            cands.append((deg, nx, ny))
    # randomize within same‐degree buckets
    random.shuffle(cands)
    cands.sort(key=lambda c: c[0])

    for _, nx, ny in cands:
        visited.add((nx,ny))
        path.append((nx,ny))
        if backtrack(path, visited, local_cap):
            return True
        path.pop()
        visited.remove((nx,ny))

    return False

# generate tours branch by branch
for first in FIRST_STEPS:
    found_branch = []
    cap = per_branch

    # seed path with the first move
    visited = {(0,0), first}
    path    = [(0,0), first]

    backtrack(path, visited, cap)

    # append up to GLOBAL_CAP tours from this branch
    for tour in found_branch:
        if GLOBAL_CAP and len(found) >= GLOBAL_CAP:
            break
        found.append([{"x": x, "y": y} for x,y in tour])
    if GLOBAL_CAP and len(found) >= GLOBAL_CAP:
        break

# write to JSON
with open("tours.json","w") as f:
    json.dump({"tours": found}, f, indent=2)

print(f"Saved {len(found)} complete tours (up to {GLOBAL_CAP or '∞'}).")
