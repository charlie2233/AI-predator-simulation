#!/usr/bin/env python3
"""
Generate a screenshot of the simulation using a virtual display.
Useful for documentation and demos.
"""
import os
import sys

# Set up virtual display
os.environ['SDL_VIDEODRIVER'] = 'dummy'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from simulation.world import World
from simulation.ui.control_panel import ControlPanel
from simulation.ui.visualization import PopulationGraph, TraitGraph
from simulation.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
    STATS_PANEL_WIDTH, BLACK, WHITE
)


def generate_screenshot(filename='simulation_screenshot.png', steps=100):
    """
    Generate a screenshot of the simulation.
    
    Args:
        filename: Output filename
        steps: Number of simulation steps to run before screenshot
    """
    print(f"Generating screenshot after {steps} simulation steps...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Create surfaces
    world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
    
    # Create world and UI
    world = World(WORLD_WIDTH, WORLD_HEIGHT)
    
    def trait_title(trait_name: str) -> str:
        """Helper to keep trait graph labeling consistent."""
        pretty_name = trait_name.replace('_', ' ').title()
        return f"Prey {pretty_name} Distribution"
    
    control_panel = ControlPanel(
        WORLD_WIDTH + 10, 10,
        STATS_PANEL_WIDTH - 20, 400
    )
    
    population_graph = PopulationGraph(
        WORLD_WIDTH + 10, 420,
        STATS_PANEL_WIDTH - 20, 150,
        species_names=list(world.populations.keys())
    )
    
    trait_graph = TraitGraph(
        WORLD_WIDTH + 10, 580,
        STATS_PANEL_WIDTH - 20, 110,
        trait_title(control_panel.get_selected_trait())
    )
    
    # Run simulation
    print(f"Running simulation...")
    current_trait = control_panel.get_selected_trait()
    for i in range(steps):
        world.update()
        if i % 10 == 0:
            population_graph.update(world)
            trait_graph.title = trait_title(current_trait)
            trait_graph.update(world.populations.get('grazer', []), current_trait)
    
    control_panel.update(world)
    
    # Draw everything
    print("Rendering...")
    screen.fill(BLACK)
    world_surface.fill(BLACK)
    
    # Draw all entities
    for food in world.food:
        food.draw(world_surface)
    for rock in world.rocks:
        rock.draw(world_surface)
    for shelter in world.shelters:
        shelter.draw(world_surface)
    for agent in world.get_all_agents():
        agent.draw(world_surface)
    
    # Blit to screen
    screen.blit(world_surface, (0, 0))
    pygame.draw.rect(screen, WHITE, (0, 0, WORLD_WIDTH, WORLD_HEIGHT), 2)
    
    # Draw UI
    control_panel.draw(screen)
    population_graph.draw(screen)
    trait_graph.draw(screen)
    
    # Add title
    font = pygame.font.Font(None, 24)
    title = font.render("AI Evolving Animals Sandbox", True, WHITE)
    screen.blit(title, (10, 10))
    
    # Save screenshot
    pygame.image.save(screen, filename)
    print(f"✅ Screenshot saved to: {filename}")
    
    # Print stats
    print(f"\nSimulation state at {steps} steps:")
    print(f"  Grazer: {len(world.populations.get('grazer', []))}")
    print(f"  Hunter: {len(world.populations.get('hunter', []))}")
    print(f"  Food: {len(world.food)}")
    
    pygame.quit()


if __name__ == "__main__":
    filename = 'simulation_screenshot.png'
    steps = 100
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            steps = int(sys.argv[2])
        except ValueError:
            print(f"Invalid step count: {sys.argv[2]}")
            sys.exit(1)
    
    generate_screenshot(filename, steps)
