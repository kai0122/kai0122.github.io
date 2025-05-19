#!/usr/bin/env python3
"""
Generate knight's tours on a 7×7 board starting at (0,0) and save them to a JSON file.

Usage:
  python generate_tours.py [max_tours]

If max_tours is omitted, the script will not stop early (i.e. collect all tours, which is
astronomically large).
"""
import json
import sys
sys.setrecursionlimit(10_000_000)

# Board size
SIZE = 7

# All eight knight moves
KNIGHT_MOVES = [
    (1, 2), (2, 1),
    (-1, 2), (-2, 1),
    (1, -2), (2, -1),
    (-1, -2), (-2, -1)
]

# Read optional max_tours from command line
try:
    MAX_TOURS = int(sys.argv[1])
    if MAX_TOURS < 1:
        MAX_TOURS = None
except (IndexError, ValueError):
    MAX_TOURS = None  # no limit

found_tours = []

def backtrack(path, visited):
    # if we hit the user-requested cap, stop
    if MAX_TOURS is not None and len(found_tours) >= MAX_TOURS:
        return True  # signal to unwind immediately

    # if we've visited every square, record this tour
    if len(path) == SIZE * SIZE:
        found_tours.append([{"x": x, "y": y} for x,y in path])
        return False  # keep searching (unless capped)

    # build Warnsdorff‐ordered candidates
    cands = []
    x0, y0 = path[-1]
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x0 + dx, y0 + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx,ny) not in visited:
            # count onward moves
            deg = 0
            for ddx, ddy in KNIGHT_MOVES:
                ax, ay = nx + ddx, ny + ddy
                if 0 <= ax < SIZE and 0 <= ay < SIZE and (ax,ay) not in visited:
                    deg += 1
            cands.append((deg, nx, ny))
    cands.sort(key=lambda c: c[0])

    for _, nx, ny in cands:
        visited.add((nx, ny))
        path.append((nx, ny))
        if backtrack(path, visited):
            return True
        path.pop()
        visited.remove((nx, ny))

    return False

def main():
    visited = {(0, 0)}
    path = [(0, 0)]
    print(f"Searching for {'up to '+str(MAX_TOURS) if MAX_TOURS else 'ALL'} tours on a {SIZE}×{SIZE} board…")
    backtrack(path, visited)
    out = {"tours": found_tours}
    with open("tours.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Done: generated {len(found_tours)} tours → tours.json")

if __name__ == "__main__":
    main()
