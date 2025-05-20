#!/usr/bin/env python3
"""
Generate knight's tours on a 7×7 board, always starting at (0,0),
sampling up to MAX_TOURS total by collecting tours from each
of the two first‐move branches.

Usage:
    python generate_tours.py [max_tours] [branch_index]

Arguments:
  max_tours     Optional integer cap on total tours (None = no cap)
  branch_index  Optional 0 or 1 to generate only the corresponding first‐move branch:
                0 => first move (1,2)
                1 => first move (2,1)
                Omit to generate both branches and write to tours.json
Outputs:
  If branch_index is provided, writes tours-<branch_index>.json
  Otherwise writes tours.json with all branches combined.
"""
import json
import sys
sys.setrecursionlimit(10_000_000)

# Board and moves
SIZE = 7
KNIGHT_MOVES = [
    (1, 2), (2, 1),
    (-1, 2), (-2, 1),
    (1, -2), (2, -1),
    (-1, -2), (-2, -1)
]
# Two valid first moves from (0,0)
FIRST_STEPS = [(1, 2), (2, 1)]

# Parse command-line arguments
try:
    MAX_TOURS = int(sys.argv[1])
    if MAX_TOURS < 1:
        MAX_TOURS = None
except (IndexError, ValueError):
    MAX_TOURS = None

try:
    BRANCH_INDEX = int(sys.argv[2])
    if BRANCH_INDEX not in (0, 1):
        raise ValueError()
except (IndexError, ValueError):
    BRANCH_INDEX = None

# How many tours per branch if we're capping?
per_branch = (MAX_TOURS // len(FIRST_STEPS)) if MAX_TOURS else None

def backtrack(path, visited, local_cap, found_branch):
    # Stop this branch if its quota is reached
    if local_cap is not None and len(found_branch) >= local_cap:
        return True  # signal to unwind early

    # If full-length, record the tour
    if len(path) == SIZE * SIZE:
        found_branch.append(path.copy())
        return False  # continue exploring (unless capped)

    # Warnsdorff heuristic: sort next moves by onward-degree
    x0, y0 = path[-1]
    candidates = []
    for dx, dy in KNIGHT_MOVES:
        nx, ny = x0 + dx, y0 + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and (nx, ny) not in visited:
            # count onward moves from (nx,ny)
            deg = 0
            for ddx, ddy in KNIGHT_MOVES:
                ax, ay = nx + ddx, ny + ddy
                if 0 <= ax < SIZE and 0 <= ay < SIZE and (ax, ay) not in visited:
                    deg += 1
            candidates.append((deg, nx, ny))
    candidates.sort(key=lambda c: c[0])

    # Try each candidate
    for _, nx, ny in candidates:
        visited.add((nx, ny))
        path.append((nx, ny))
        if backtrack(path, visited, local_cap, found_branch):
            return True
        path.pop()
        visited.remove((nx, ny))

    return False

def main():
    print(f"Starting generation: cap={MAX_TOURS}, branch={BRANCH_INDEX}")
    all_found = []

    # Loop over first-move branches
    for i, first in enumerate(FIRST_STEPS):
        # If user specified a branch, skip the other
        if BRANCH_INDEX is not None and i != BRANCH_INDEX:
            continue

        print(f"  → Generating branch {i}, first move {first}")
        found_branch = []
        cap = per_branch if MAX_TOURS else None

        # Seed path and visited
        visited = {(0, 0), first}
        path = [(0, 0), first]

        # Backtrack to collect tours for this branch
        backtrack(path, visited, cap, found_branch)

        # Append to global list (respect MAX_TOURS)
        for tour in found_branch:
            if MAX_TOURS and len(all_found) >= MAX_TOURS:
                break
            all_found.append(tour)
        if MAX_TOURS and len(all_found) >= MAX_TOURS:
            break

    # Prepare output filename
    if BRANCH_INDEX is not None:
        out_name = f"tours-{BRANCH_INDEX}.json"
    else:
        out_name = "tours.json"

    # Convert to JSON‐friendly format
    output = {
        "tours": [
            [{"x": x, "y": y} for x, y in tour]
            for tour in all_found
        ]
    }

    # Write file
    with open(out_name, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done! Generated {len(all_found)} tours → {out_name}")

if __name__ == "__main__":
    main()
