"""
Visualization components for statistics and graphs.
"""
import pygame
from collections import deque
from simulation.config import WHITE, DARK_GRAY, SPECIES_STYLE


class PopulationGraph:
    """Real-time population graph."""
    
    def __init__(self, x, y, width, height, species_names, max_history=200):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_history = max_history
        self.history = {name: deque(maxlen=max_history) for name in species_names}
        self.food_history = deque(maxlen=max_history)
        self.font = None
        self.species_names = species_names
    
    def update(self, world):
        for name in self.species_names:
            self.history[name].append(len(world.populations.get(name, [])))
        self.food_history.append(len(world.food))
    
    def draw(self, surface):
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        title = self.font.render("Population History", True, WHITE)
        surface.blit(title, (self.rect.x + 5, self.rect.y + 5))
        if not self.history or len(next(iter(self.history.values()))) < 2:
            return
        max_val = max(max(max(hist) if hist else [1]) for hist in self.history.values())
        max_val = max(max_val, max(self.food_history) if self.food_history else 1, 10)
        for i in range(5):
            y = self.rect.y + 25 + (self.rect.height - 30) * i // 4
            pygame.draw.line(surface, (80, 80, 80), (self.rect.x + 5, y), (self.rect.right - 5, y), 1)
            label = self.font.render(str(int(max_val * (4 - i) / 4)), True, WHITE)
            surface.blit(label, (self.rect.x + 5, y - 8))
        for name, hist in self.history.items():
            color = SPECIES_STYLE.get(name, {}).get("color", WHITE)
            self.draw_line(surface, hist, max_val, color)
        self.draw_line(surface, self.food_history, max_val, (200, 200, 50))
        legend_y = self.rect.bottom - 20
        offset = 0
        for name in self.species_names:
            color = SPECIES_STYLE.get(name, {}).get("color", WHITE)
            self.draw_legend_item(surface, self.rect.x + 60 + offset, legend_y, color, name.title())
            offset += 90
        self.draw_legend_item(surface, self.rect.x + 60 + offset, legend_y, (200, 200, 50), "Food")
    
    def draw_line(self, surface, history, max_val, color):
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


class LogPanel:
    """Displays recent log messages (extinctions, generation summaries)."""

    def __init__(self, x, y, width, height, max_lines=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_lines = max_lines
        self.font = None
        self.lines = deque(maxlen=max_lines)

    def push(self, message: str):
        self.lines.appendleft(message)

    def draw(self, surface):
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        pygame.draw.rect(surface, DARK_GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        title = self.font.render("Events", True, WHITE)
        surface.blit(title, (self.rect.x + 5, self.rect.y + 5))
        for i, line in enumerate(self.lines):
            txt = self.font.render(line, True, WHITE)
            surface.blit(txt, (self.rect.x + 5, self.rect.y + 25 + i * 16))
