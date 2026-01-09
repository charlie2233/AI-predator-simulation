#!/usr/bin/env python3
"""
Headless smoke test for the evolving sandbox.
Runs a few generations and prints summaries.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation.world import World


def run_headless_test(generations=5):
    world = World()
    print("Running headless smoke test...")
    for _ in range(generations):
        target_generation = world.generation + 1
        while world.generation < target_generation:
            world.update()
        counts = {sp: len(world.populations.get(sp, [])) for sp in world.populations.keys()}
        print(f"Gen {world.generation - 1} summary: {counts}")
        if any(v == 0 for v in counts.values()):
            print("  Extinction recovered (archive) triggered.")
    print("Smoke test complete.")


if __name__ == "__main__":
    gens = 5
    if len(sys.argv) > 1:
        try:
            gens = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_headless.py [generations]")
            sys.exit(1)
    run_headless_test(gens)
