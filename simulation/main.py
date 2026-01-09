"""
Main simulation runner with pygame interface.
"""
import pygame
import sys
from simulation.world import World
from simulation.ui.control_panel import ControlPanel
from simulation.ui.visualization import PopulationGraph, TraitGraph
from simulation.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
    STATS_PANEL_WIDTH, FPS, BLACK, WHITE
)


class Simulation:
    """Main simulation controller."""
    
    def __init__(self):
        """Initialize the simulation."""
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Predator-Prey Simulation")
        
        # Create surfaces
        self.world_surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Create world
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        
        # Create UI components
        self.control_panel = ControlPanel(
            WORLD_WIDTH + 10, 10,
            STATS_PANEL_WIDTH - 20, 400
        )
        
        self.population_graph = PopulationGraph(
            WORLD_WIDTH + 10, 420,
            STATS_PANEL_WIDTH - 20, 150
        )
        
        self.trait_graph = TraitGraph(
            WORLD_WIDTH + 10, 580,
            STATS_PANEL_WIDTH - 20, 110,
            "Prey Speed Distribution"
        )
        
        # Simulation state
        self.running = True
        self.paused = False
        self.update_counter = 0
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.world.reset()
            
            # Handle UI events
            actions = self.control_panel.handle_event(event)
            
            if actions.get('toggle_pause'):
                self.paused = self.control_panel.paused
            
            if actions.get('reset'):
                self.world.reset()
                self.population_graph.prey_history.clear()
                self.population_graph.predator_history.clear()
                self.population_graph.food_history.clear()
    
    def update(self):
        """Update simulation state."""
        if not self.paused:
            # Update world based on simulation speed
            speed = int(self.control_panel.simulation_speed)
            for _ in range(max(1, speed)):
                self.world.update()
            
            # Update UI components periodically
            self.update_counter += 1
            if self.update_counter % 10 == 0:
                self.population_graph.update(self.world)
                self.trait_graph.update(self.world.prey, 'speed')
        
        # Always update control panel
        self.control_panel.update(self.world)
    
    def draw(self):
        """Draw all visual elements."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw world
        self.world_surface.fill(BLACK)
        
        # Draw all food
        for food in self.world.food:
            food.draw(self.world_surface)
        
        # Draw all prey
        for prey in self.world.prey:
            prey.draw(self.world_surface)
        
        # Draw all predators
        for predator in self.world.predators:
            predator.draw(self.world_surface)
        
        # Blit world surface to screen
        self.screen.blit(self.world_surface, (0, 0))
        
        # Draw world border
        pygame.draw.rect(self.screen, WHITE, (0, 0, WORLD_WIDTH, WORLD_HEIGHT), 2)
        
        # Draw UI components
        self.control_panel.draw(self.screen)
        self.population_graph.draw(self.screen)
        self.trait_graph.draw(self.screen)
        
        # Draw FPS counter
        fps_font = pygame.font.Font(None, 20)
        fps_text = fps_font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main simulation loop."""
        print("=" * 60)
        print("AI Predator-Prey Simulation")
        print("=" * 60)
        print("\nControls:")
        print("  SPACE     - Pause/Resume")
        print("  R         - Reset simulation")
        print("  ESC       - Quit")
        print("\nUI Controls:")
        print("  Speed slider - Adjust simulation speed")
        print("  Pause button - Pause/Resume simulation")
        print("  Reset button - Reset simulation")
        print("\nFeatures:")
        print("  • Genetic evolution with traits (speed, vision, efficiency)")
        print("  • Multiple species (herbivores, carnivores, omnivores)")
        print("  • Real-time population graphs")
        print("  • Trait distribution visualization")
        print("  • Control panel for adjusting parameters")
        print("\n" + "=" * 60)
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the simulation."""
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()
