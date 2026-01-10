"""
Non-living world elements like rocks and shelters.
"""
import pygame
import random
import math
from simulation.config import SHELTER_RADIUS, LIGHT_GRAY, DARK_GRAY


class Rock:
    """Resource node that can be converted into a shelter."""

    def __init__(self, x, y, size=8):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True
        self.variation = random.random()  # For visual variety

    def draw(self, surface):
        if not self.alive:
            return
        
        pos = (int(self.x), int(self.y))
        
        # Rock color palette - grays and browns
        base_color = (150, 140, 130)
        dark_color = (110, 100, 90)
        highlight_color = (180, 170, 160)
        
        # Shadow
        shadow_offset = 2
        pygame.draw.circle(surface, (40, 40, 40), (pos[0] + shadow_offset, pos[1] + shadow_offset), self.size)
        
        # Main rock body - irregular shape using overlapping circles
        points = []
        num_points = 6
        for i in range(num_points):
            angle = (i / num_points) * math.pi * 2
            variation = 0.8 + self.variation * 0.4
            radius = self.size * variation
            px = pos[0] + int(math.cos(angle) * radius)
            py = pos[1] + int(math.sin(angle) * radius)
            points.append((px, py))
        
        # Draw as polygon for irregular shape
        pygame.draw.polygon(surface, dark_color, points)
        
        # Gradient effect - lighter on top
        for i in range(3):
            shrink = i + 1
            inner_points = []
            for j in range(num_points):
                angle = (j / num_points) * math.pi * 2
                variation = 0.7 + self.variation * 0.3
                radius = (self.size - shrink) * variation
                px = pos[0] + int(math.cos(angle) * radius)
                py = pos[1] - shrink + int(math.sin(angle) * radius)
                inner_points.append((px, py))
            
            if len(inner_points) > 2:
                brightness = 1.0 + i * 0.15
                grad_color = tuple(min(255, int(c * brightness)) for c in base_color)
                pygame.draw.polygon(surface, grad_color, inner_points)
        
        # Highlight spot
        highlight_pos = (pos[0] - self.size // 3, pos[1] - self.size // 3)
        pygame.draw.circle(surface, highlight_color, highlight_pos, max(2, self.size // 4))


class Shelter:
    """Shelter that gives nearby agents disaster protection."""

    def __init__(self, x, y, radius=SHELTER_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius
        self.alive = True
        self.pillar_count = 6

    def draw(self, surface):
        if not self.alive:
            return
        
        pos = (int(self.x), int(self.y))
        
        # Shelter colors
        structure_color = (90, 80, 70)
        roof_color = (120, 110, 100)
        shadow_color = (30, 30, 30)
        
        # Protection radius indicator (subtle)
        for i in range(3, 0, -1):
            alpha_surface = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
            alpha = 15 * i
            circle_color = (*LIGHT_GRAY, alpha)
            pygame.draw.circle(alpha_surface, circle_color, (self.radius + 5, self.radius + 5), self.radius * i // 3, 1)
            surface.blit(alpha_surface, (pos[0] - self.radius - 5, pos[1] - self.radius - 5))
        
        # Draw pillars in a circle
        pillar_radius = self.radius // 2
        for i in range(self.pillar_count):
            angle = (i / self.pillar_count) * math.pi * 2
            pillar_x = pos[0] + int(math.cos(angle) * pillar_radius)
            pillar_y = pos[1] + int(math.sin(angle) * pillar_radius)
            
            # Pillar shadow
            pygame.draw.rect(surface, shadow_color, 
                           (pillar_x - 2, pillar_y - 5, 5, 12))
            
            # Pillar
            pygame.draw.rect(surface, structure_color, 
                           (pillar_x - 2, pillar_y - 6, 4, 12), border_radius=1)
            # Highlight on pillar
            pygame.draw.line(surface, (130, 120, 110), 
                           (pillar_x - 1, pillar_y - 6), 
                           (pillar_x - 1, pillar_y + 4), 1)
        
        # Central roof dome
        pygame.draw.circle(surface, shadow_color, (pos[0] + 2, pos[1] + 2), self.radius // 3)
        
        # Roof gradient
        for i in range(self.radius // 3, 0, -1):
            ratio = i / (self.radius // 3)
            roof_grad = tuple(min(255, int(c * (0.8 + ratio * 0.2))) for c in roof_color)
            pygame.draw.circle(surface, roof_grad, pos, i)
        
        # Roof highlight
        highlight_pos = (pos[0] - self.radius // 6, pos[1] - self.radius // 6)
        pygame.draw.circle(surface, (160, 150, 140), highlight_pos, max(2, self.radius // 8))
        
        # Center post/flag
        pygame.draw.line(surface, (140, 130, 120), 
                        (pos[0], pos[1] - self.radius // 3), 
                        (pos[0], pos[1] - self.radius), 2)
        # Small flag
        flag_top = pos[1] - self.radius
        flag_points = [
            (pos[0], flag_top),
            (pos[0] + 6, flag_top + 3),
            (pos[0], flag_top + 6)
        ]
        pygame.draw.polygon(surface, (139, 233, 253), flag_points)
