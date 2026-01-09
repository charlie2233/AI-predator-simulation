#!/usr/bin/env python3
"""
Headless test script for the simulation.
This runs the simulation without GUI for testing purposes.
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation.world import World
from simulation.evolution.genetics import EvolutionTracker


def run_headless_test(steps=500):
    """
    Run simulation without GUI for testing.
    
    Args:
        steps: Number of simulation steps to run
    """
    print("=" * 70)
    print("AI Predator-Prey Simulation - Headless Test")
    print("=" * 70)
    
    # Create world
    world = World(800, 600)
    
    print(f"\nInitial State:")
    print(f"  Prey: {len(world.prey)}")
    print(f"  Predators: {len(world.predators)}")
    print(f"  Food: {len(world.food)}")
    
    print(f"\nRunning {steps} simulation steps...")
    
    # Track statistics
    report_interval = steps // 10
    
    # Cache for average calculations
    cached_prey_speed = 0
    cached_pred_speed = 0
    
    for step in range(steps):
        world.update()
        
        # Report progress
        if step % report_interval == 0:
            # Calculate averages only when reporting
            cached_prey_speed = (sum(p.traits.speed for p in world.prey) / len(world.prey)) if world.prey else 0
            cached_pred_speed = (sum(p.traits.speed for p in world.predators) / len(world.predators)) if world.predators else 0
            
            print(f"  Step {step:4d}: "
                  f"Prey={len(world.prey):3d} (speed={cached_prey_speed:.2f}), "
                  f"Predators={len(world.predators):3d} (speed={cached_pred_speed:.2f}), "
                  f"Food={len(world.food):3d}")
    
    # Final report
    print(f"\n{'=' * 70}")
    print("Final Statistics:")
    print(f"{'=' * 70}")
    print(f"  Total Steps: {world.time_step}")
    print(f"  Current Population:")
    print(f"    Prey: {len(world.prey)}")
    print(f"    Predators: {len(world.predators)}")
    print(f"    Food: {len(world.food)}")
    print(f"\n  Lifetime Statistics:")
    print(f"    Prey born: {world.stats['prey_born']}")
    print(f"    Prey died: {world.stats['prey_died']}")
    print(f"    Predators born: {world.stats['predators_born']}")
    print(f"    Predators died: {world.stats['predators_died']}")
    
    if world.prey:
        print(f"\n  Average Prey Traits:")
        print(f"    Speed: {sum(p.traits.speed for p in world.prey) / len(world.prey):.2f}")
        print(f"    Vision: {sum(p.traits.vision for p in world.prey) / len(world.prey):.2f}")
        print(f"    Energy Efficiency: {sum(p.traits.energy_efficiency for p in world.prey) / len(world.prey):.2f}")
        print(f"    Size: {sum(p.traits.size for p in world.prey) / len(world.prey):.2f}")
    
    if world.predators:
        print(f"\n  Average Predator Traits:")
        print(f"    Speed: {sum(p.traits.speed for p in world.predators) / len(world.predators):.2f}")
        print(f"    Vision: {sum(p.traits.vision for p in world.predators) / len(world.predators):.2f}")
        print(f"    Energy Efficiency: {sum(p.traits.energy_efficiency for p in world.predators) / len(world.predators):.2f}")
        print(f"    Size: {sum(p.traits.size for p in world.predators) / len(world.predators):.2f}")
    
    print(f"\n{'=' * 70}")
    print("✅ Test completed successfully!")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    steps = 500
    if len(sys.argv) > 1:
        try:
            steps = int(sys.argv[1])
        except ValueError:
            print(f"Invalid step count: {sys.argv[1]}")
            print("Usage: python test_headless.py [steps]")
            sys.exit(1)
    
    run_headless_test(steps)
