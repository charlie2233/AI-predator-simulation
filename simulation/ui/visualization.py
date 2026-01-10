"""
Visualization components for statistics and graphs.
"""
import pygame
from collections import deque
from simulation.config import (
    WHITE, DARK_GRAY, SPECIES_STYLE,
    UI_BG_COLOR, UI_PANEL_BG, UI_TEXT_COLOR, UI_BORDER_COLOR,
    UI_ACCENT_COLOR, ORANGE
)


class PopulationGraph:
    """Real-time population graph."""
    
    def __init__(self, x, y, width, height, species_names, max_history=200):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_history = max_history
        self.history = {name: deque(maxlen=max_history) for name in species_names}
        self.food_history = deque(maxlen=max_history)
        self.reset_marks = deque(maxlen=max_history)
        self.font = None
        self.species_names = species_names
    
    def update(self, world):
        for name in self.species_names:
            self.history[name].append(len(world.populations.get(name, [])))
        self.food_history.append(len(world.food))

    def add_reset_mark(self):
        """Mark a vertical line for generation/reset events."""
        self.reset_marks.append(len(self.food_history))
    
    def draw(self, surface):
        if not self.font:
            self.font = pygame.font.Font(None, 16)
            
        # Background with subtle gradient
        bg_surf = pygame.Surface((self.rect.width, self.rect.height))
        for i in range(self.rect.height):
            ratio = i / self.rect.height
            color = tuple(int(UI_PANEL_BG[j] * (1 + ratio * 0.1)) for j in range(3))
            pygame.draw.line(bg_surf, color, (0, i), (self.rect.width, i))
        surface.blit(bg_surf, self.rect.topleft)
        
        # Border with glow
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=8)
        
        title = self.font.render("Population History", True, UI_TEXT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 8))
        
        if not self.history or len(next(iter(self.history.values()))) < 2:
            return
            
        # Safe max to avoid int/list mix
        series_max = 1
        for hist in self.history.values():
            if hist:
                series_max = max(series_max, max(hist))
        food_max = max(self.food_history) if self.food_history else 1
        max_val = max(series_max, food_max, 10)
        
        # Grid lines
        for i in range(5):
            y = self.rect.y + 30 + (self.rect.height - 40) * i // 4
            pygame.draw.line(surface, (60, 60, 70), (self.rect.x + 5, y), (self.rect.right - 5, y), 1)
            label = self.font.render(str(int(max_val * (4 - i) / 4)), True, (150, 150, 160))
            surface.blit(label, (self.rect.x + 8, y - 8))
            
        # Draw lines
        for name, hist in self.history.items():
            color = SPECIES_STYLE.get(name, {}).get("color", WHITE)
            self.draw_line(surface, hist, max_val, color)
        self.draw_line(surface, self.food_history, max_val, ORANGE)
        self._draw_marks(surface)
        
        # Legend
        legend_y = self.rect.bottom - 20
        offset = 0
        start_x = self.rect.x + 60
        
        for name in self.species_names:
            color = SPECIES_STYLE.get(name, {}).get("color", WHITE)
            self.draw_legend_item(surface, start_x + offset, legend_y, color, name.title())
            offset += 75
            
        self.draw_legend_item(surface, start_x + offset, legend_y, ORANGE, "Food")
    
    def draw_line(self, surface, history, max_val, color):
        if len(history) < 2:
            return
        points = []
        graph_height = self.rect.height - 40
        graph_width = self.rect.width - 20
        
        for i, value in enumerate(history):
            x = self.rect.x + 10 + (i * graph_width) // self.max_history
            y = self.rect.y + 30 + graph_height - int((value / max_val) * graph_height)
            points.append((x, y))
            
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 2)

    def _draw_marks(self, surface):
        if not self.reset_marks:
            return
        graph_width = self.rect.width - 20
        for mark in self.reset_marks:
            x = self.rect.x + 10 + (mark * graph_width) // max(1, self.max_history)
            pygame.draw.line(surface, UI_ACCENT_COLOR, (x, self.rect.y + 25), (x, self.rect.bottom - 25), 1)
    
    def draw_legend_item(self, surface, x, y, color, text):
        pygame.draw.circle(surface, color, (x + 5, y + 5), 4)
        label = self.font.render(text, True, UI_TEXT_COLOR)
        surface.blit(label, (x + 12, y - 2))


class TraitGraph:
    """Graph for displaying evolution of traits."""
    
    def __init__(self, x, y, width, height, title="Trait Evolution"):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = None
        
        self.trait_data = {}
        # Using the same pastel palette for traits roughly
        self.colors = {
            'speed': (139, 233, 253), # Cyan
            'vision': (255, 184, 108), # Orange
            'energy_efficiency': (189, 147, 249), # Purple
            'size': (80, 250, 123) # Green
        }
    
    def update(self, agents, trait_name):
        if not agents:
            self.trait_data = {}
            return
        
        # Collect trait values
        values = []
        for agent in agents:
            dna_val = agent.dna.genes.get(trait_name)
            if dna_val is not None:
                values.append(dna_val)
        if not values:
            self.trait_data = {}
            return
        
        # Create histogram bins
        min_val = min(values)
        max_val = max(values)
        num_bins = 15 # More resolution
        
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
        if not self.font:
            self.font = pygame.font.Font(None, 16)
        
        # Draw background
        pygame.draw.rect(surface, UI_PANEL_BG, self.rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=8)
        
        # Draw title
        title = self.font.render(self.title, True, UI_TEXT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 8))
        
        if not self.trait_data:
            return
        
        bins = self.trait_data['bins']
        max_count = max(bins) if bins else 1
        
        # Draw histogram bars
        # width minus padding
        graph_width = self.rect.width - 20
        bar_width = graph_width // len(bins)
        
        for i, count in enumerate(bins):
            if count > 0:
                bar_height = int((count / max_count) * (self.rect.height - 50))
                bar_x = self.rect.x + 10 + i * bar_width
                bar_y = self.rect.bottom - 20 - bar_height
                
                color = self.colors.get(self.trait_data['trait'], UI_ACCENT_COLOR)
                
                # Bar with rounded top
                bar_rect = pygame.Rect(bar_x, bar_y, bar_width - 1, bar_height)
                pygame.draw.rect(surface, color, bar_rect, border_top_left_radius=3, border_top_right_radius=3)
        
        # Draw axis labels
        min_label = self.font.render(f"{self.trait_data['min']:.1f}", True, (150, 150, 160))
        max_label = self.font.render(f"{self.trait_data['max']:.1f}", True, (150, 150, 160))
        surface.blit(min_label, (self.rect.x + 10, self.rect.bottom - 18))
        surface.blit(max_label, (self.rect.right - 30, self.rect.bottom - 18))


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
        
        pygame.draw.rect(surface, UI_PANEL_BG, self.rect, border_radius=8)
        pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 2, border_radius=8)
        
        title = self.font.render("Events Log", True, UI_ACCENT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 8))
        
        for i, line in enumerate(self.lines):
            # Fade out older lines
            alpha = 255 - (i * 30)
            if alpha < 0: alpha = 0
            
            # Since we can't easily alpha text in pygame without surfaces, we'll just use color
            color = UI_TEXT_COLOR
            if i > 2:
                color = (150, 150, 160)
            
            txt = self.font.render(line, True, color)
            surface.blit(txt, (self.rect.x + 10, self.rect.y + 30 + i * 16))
