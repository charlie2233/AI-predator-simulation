"""
Visualization components for statistics and graphs.
"""
import pygame
from collections import deque
from simulation.config import WHITE, GREEN, RED, BLUE, YELLOW, DARK_GRAY


class PopulationGraph:
    """Real-time population graph."""
    
    def __init__(self, x, y, width, height, max_history=200):
        """
        Initialize population graph.
        
        Args:
            x: X position
            y: Y position
            width: Graph width
            height: Graph height
            max_history: Maximum history points to display
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.max_history = max_history
        
        self.prey_history = deque(maxlen=max_history)
        self.predator_history = deque(maxlen=max_history)
        self.food_history = deque(maxlen=max_history)
        
        self.font = None
    
    def update(self, world):
        """
        Update graph data.
        
        Args:
            world: World instance
        """
        self.prey_history.append(len(world.prey))
        self.predator_history.append(len(world.predators))
        self.food_history.append(len(world.food))
    
    def draw(self, surface):
        """
        Draw the population graph.
        
        Args:
            surface: Pygame surface
        """
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw title
        title = self.font.render("Population History", True, WHITE)
        surface.blit(title, (self.rect.x + 5, self.rect.y + 5))
        
        if len(self.prey_history) < 2:
            return
        
        # Find max value for scaling
        max_val = max(
            max(self.prey_history) if self.prey_history else 1,
            max(self.predator_history) if self.predator_history else 1,
            max(self.food_history) if self.food_history else 1,
            10  # Minimum scale
        )
        
        # Draw grid lines
        for i in range(5):
            y = self.rect.y + 25 + (self.rect.height - 30) * i // 4
            pygame.draw.line(surface, (80, 80, 80), 
                           (self.rect.x + 5, y), 
                           (self.rect.right - 5, y), 1)
            label = self.font.render(str(int(max_val * (4 - i) / 4)), True, WHITE)
            surface.blit(label, (self.rect.x + 5, y - 8))
        
        # Draw data lines
        self.draw_line(surface, self.prey_history, max_val, GREEN)
        self.draw_line(surface, self.predator_history, max_val, RED)
        self.draw_line(surface, self.food_history, max_val, YELLOW)
        
        # Draw legend
        legend_y = self.rect.bottom - 20
        self.draw_legend_item(surface, self.rect.x + 60, legend_y, GREEN, "Prey")
        self.draw_legend_item(surface, self.rect.x + 140, legend_y, RED, "Predators")
        self.draw_legend_item(surface, self.rect.x + 240, legend_y, YELLOW, "Food")
    
    def draw_line(self, surface, history, max_val, color):
        """
        Draw a data line on the graph.
        
        Args:
            surface: Pygame surface
            history: Data history deque
            max_val: Maximum value for scaling
            color: Line color
        """
        if len(history) < 2:
            return
        
        points = []
        graph_height = self.rect.height - 30
        graph_width = self.rect.width - 10
        
        for i, value in enumerate(history):
            x = self.rect.x + 5 + (i * graph_width) // self.max_history
            y = self.rect.y + 25 + graph_height - int((value / max_val) * graph_height)
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 2)
    
    def draw_legend_item(self, surface, x, y, color, text):
        """
        Draw a legend item.
        
        Args:
            surface: Pygame surface
            x: X position
            y: Y position
            color: Color for the item
            text: Legend text
        """
        pygame.draw.rect(surface, color, (x, y, 10, 10))
        label = self.font.render(text, True, WHITE)
        surface.blit(label, (x + 15, y - 2))


class TraitGraph:
    """Graph for displaying evolution of traits."""
    
    def __init__(self, x, y, width, height, title="Trait Evolution"):
        """
        Initialize trait graph.
        
        Args:
            x: X position
            y: Y position
            width: Graph width
            height: Graph height
            title: Graph title
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = None
        
        self.trait_data = {}
        self.colors = {
            'speed': (100, 200, 255),
            'vision': (255, 200, 100),
            'energy_efficiency': (200, 100, 255),
            'size': (100, 255, 200)
        }
    
    def update(self, agents, trait_name):
        """
        Update trait distribution data.
        
        Args:
            agents: List of agents
            trait_name: Name of trait to display
        """
        if not agents:
            self.trait_data = {}
            return
        
        # Collect trait values
        values = [getattr(agent.traits, trait_name) for agent in agents]
        
        # Create histogram bins
        min_val = min(values)
        max_val = max(values)
        num_bins = 10
        
        if max_val - min_val < 0.01:
            self.trait_data = {}
            return
        
        bin_width = (max_val - min_val) / num_bins
        bins = [0] * num_bins
        
        for value in values:
            bin_index = min(int((value - min_val) / bin_width), num_bins - 1)
            bins[bin_index] += 1
        
        self.trait_data = {
            'bins': bins,
            'min': min_val,
            'max': max_val,
            'trait': trait_name
        }
    
    def draw(self, surface):
        """
        Draw the trait graph.
        
        Args:
            surface: Pygame surface
        """
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        
        # Draw background
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        # Draw title
        title = self.font.render(self.title, True, WHITE)
        surface.blit(title, (self.rect.x + 5, self.rect.y + 5))
        
        if not self.trait_data:
            return
        
        bins = self.trait_data['bins']
        max_count = max(bins) if bins else 1
        
        # Draw histogram bars
        bar_width = (self.rect.width - 20) // len(bins)
        for i, count in enumerate(bins):
            if count > 0:
                bar_height = int((count / max_count) * (self.rect.height - 40))
                bar_x = self.rect.x + 10 + i * bar_width
                bar_y = self.rect.bottom - 10 - bar_height
                
                color = self.colors.get(self.trait_data['trait'], WHITE)
                pygame.draw.rect(surface, color, 
                               (bar_x, bar_y, bar_width - 2, bar_height))
        
        # Draw axis labels
        min_label = self.font.render(f"{self.trait_data['min']:.1f}", True, WHITE)
        max_label = self.font.render(f"{self.trait_data['max']:.1f}", True, WHITE)
        surface.blit(min_label, (self.rect.x + 10, self.rect.bottom - 25))
        surface.blit(max_label, (self.rect.right - 40, self.rect.bottom - 25))
