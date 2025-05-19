#!/usr/bin/env python3
"""
Generate knight's tours on a 7×7 board starting at (0,0) and save them to a JSON file.

WARNING: The total number of complete tours on a 7×7 board is enormous. Enumerating them all
can take extremely long and consume lots of memory.

This script supports a `MAX_TOURS` limit so you can generate only the first N tours and
inspect them locally.

Usage:
  python generate_tours.py [max_tours]

If `max_tours` is not provided or invalid, the script defaults to 8 tours (maximum cap).

Output:
  Creates `tours.json` in the current directory with structure:
    {
      "tours": [
         [ {"x":0, "y":0}, {"x":1, "y":2}, … ],
         … up to MAX_TOURS tours …
      ]
    }
"""
import json
import sys

# Board size\SIZE = 7
# All eight knight moves
KNIGHT_MOVES = [
    (1, 2), (2, 1),
    (-1, 2), (-2, 1),
    (1, -2), (2, -1),
    (-1, -2), (-2, -1)
]

# Limit on number of tours to generate (capped at 8)
try:
    MAX_TOURS = min(int(sys.argv[1]), 8)
except (IndexError, ValueError):
    MAX_TOURS = 8

# Collected tours will be stored here
# Each tour is a list of (x,y) tuples
found_tours = []
SIZE = 7

# Backtracking with Warnsdorff's heuristic

def backtrack(path, visited):
    # Early exit if we've collected enough
    if len(found_tours) >= MAX_TOURS:
        return True  # signal to stop

    # If full length, record the tour
    if len(path) == SIZE * SIZE:
        tour_dicts = [{"x": x, "y": y} for (x, y) in path]
        found_tours.append(tour_dicts)
        return False

    # Generate candidates ordered by onward degree (Warnsdorff)
    candidates = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = path[-1][0] + dx, path[-1][1] + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx, ny) not in visited:
            deg = 0
            for ddx, ddy in KNIGHT_MOVES:
                ax, ay = nx + ddx, ny + ddy
                if 0 <= ax < SIZE and 0 <= ay < SIZE and (ax, ay) not in visited:
                    deg += 1
            candidates.append((deg, nx, ny))
    candidates.sort(key=lambda c: c[0])

    for _, nx, ny in candidates:
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
    print(f"Starting search for up to {MAX_TOURS} tours on a {SIZE}×{SIZE} board...")
    backtrack(path, visited)
    output = {"tours": found_tours}
    with open("tours.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Generated {len(found_tours)} tours; saved to tours.json")


if __name__ == "__main__":
    main()
