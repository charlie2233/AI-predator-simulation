"""
Food items for the simulation.
"""
import pygame
import random
import math
from simulation.config import (
    FOOD_SIZE,
    FOOD_ENERGY_VALUE,
    FOOD_COLOR,
    CARCASS_COLOR,
    FOOD_SIZE_RANGE,
    FOOD_ENERGY_RANGE,
    TREE_SIZE_RANGE,
    TREE_ENERGY_VALUE,
)


class Food:
    """Food item (plant or carcass)."""

    def __init__(self, x, y, energy_value=FOOD_ENERGY_VALUE, is_carcass=False, size=None):
        """
        Initialize food item.

        Args:
            x: X position
            y: Y position
            energy_value: Energy to grant
            is_carcass: Whether this is a carcass drop
            size: Optional explicit size
        """
        self.x = x
        self.y = y
        self.alive = True
        self.energy_value = energy_value
        self.size = size if size is not None else FOOD_SIZE
        self.is_carcass = is_carcass
        self.bob_offset = random.uniform(0, math.pi * 2)  # For animation

    def draw(self, surface):
        if not self.alive:
            return
        
        pos = (int(self.x), int(self.y))
        
        if self.is_carcass:
            # Carcass - scattered bone-like appearance
            color = CARCASS_COLOR
            # Main pile
            for i in range(3):
                offset_x = random.randint(-self.size // 2, self.size // 2)
                offset_y = random.randint(-self.size // 2, self.size // 2)
                pygame.draw.circle(surface, color, (pos[0] + offset_x, pos[1] + offset_y), self.size // 2)
            # Darker outline
            pygame.draw.circle(surface, (180, 140, 80), pos, self.size, 1)
        else:
            # Berry-like food with shine
            color = FOOD_COLOR
            
            # Shadow
            shadow_pos = (pos[0] + 1, pos[1] + 1)
            pygame.draw.circle(surface, (80, 100, 80), shadow_pos, self.size)
            
            # Main berry body - gradient effect
            for i in range(self.size, 0, -1):
                ratio = i / self.size
                grad_color = tuple(min(255, int(c * (0.7 + ratio * 0.3))) for c in color)
                pygame.draw.circle(surface, grad_color, pos, i)
            
            # Shine spot
            shine_pos = (pos[0] - self.size // 3, pos[1] - self.size // 3)
            pygame.draw.circle(surface, (200, 255, 200), shine_pos, max(1, self.size // 3))
            
            # Small stem on top
            stem_color = (90, 140, 70)
            stem_start = (pos[0], pos[1] - self.size)
            stem_end = (pos[0], pos[1] - self.size - 2)
            pygame.draw.line(surface, stem_color, stem_start, stem_end, 2)


class PlantFood(Food):
    """Larger plant/tree-like food with beautiful rendering."""

    def __init__(self, x, y, size=None, energy_value=TREE_ENERGY_VALUE):
        size = size if size is not None else random.randint(*TREE_SIZE_RANGE)
        super().__init__(x, y, energy_value=energy_value, is_carcass=False, size=size)
        self.leaf_count = random.randint(5, 8)
        self.leaf_angles = [random.uniform(0, math.pi * 2) for _ in range(self.leaf_count)]

    def draw(self, surface):
        if not self.alive:
            return
        
        pos = (int(self.x), int(self.y))
        
        # Trunk - with texture
        trunk_width = max(3, self.size // 3)
        trunk_height = max(6, self.size)
        trunk_color = (120, 90, 60)
        trunk_dark = (90, 70, 50)
        
        # Trunk shadow
        shadow_rect = pygame.Rect(pos[0] - trunk_width // 2 + 2, pos[1] + 2, trunk_width, trunk_height)
        pygame.draw.rect(surface, (40, 30, 25), shadow_rect, border_radius=2)
        
        # Main trunk with gradient
        trunk_rect = pygame.Rect(pos[0] - trunk_width // 2, pos[1], trunk_width, trunk_height)
        pygame.draw.rect(surface, trunk_color, trunk_rect, border_radius=2)
        # Bark lines
        for i in range(3):
            line_y = pos[1] + trunk_height // 4 * (i + 1)
            pygame.draw.line(surface, trunk_dark, 
                           (pos[0] - trunk_width // 2, line_y),
                           (pos[0] + trunk_width // 2, line_y), 1)
        
        # Leaves/crown - fluffy cloud-like appearance
        crown_center = (pos[0], pos[1])
        
        # Multiple leaf clusters for depth
        for i, angle in enumerate(self.leaf_angles):
            offset_dist = self.size // 3
            leaf_x = pos[0] + int(math.cos(angle) * offset_dist)
            leaf_y = pos[1] + int(math.sin(angle) * offset_dist)
            
            # Darker back leaves
            back_color = (100, 200, 100)
            pygame.draw.circle(surface, back_color, (leaf_x + 1, leaf_y + 1), self.size // 2)
        
        # Main crown with gradient
        for i in range(self.size, 0, -1):
            ratio = i / self.size
            green_intensity = int(180 + ratio * 70)
            crown_color = (min(255, green_intensity - 100), min(255, green_intensity), min(255, green_intensity - 100))
            pygame.draw.circle(surface, crown_color, crown_center, i)
        
        # Highlight on crown
        highlight_pos = (pos[0] - self.size // 4, pos[1] - self.size // 4)
        pygame.draw.circle(surface, (180, 255, 180), highlight_pos, self.size // 3)
        
        # Small fruits on tree
        for i in range(3):
            fruit_angle = random.uniform(0, math.pi * 2)
            fruit_dist = self.size // 2
            fruit_x = pos[0] + int(math.cos(fruit_angle) * fruit_dist)
            fruit_y = pos[1] + int(math.sin(fruit_angle) * fruit_dist)
            pygame.draw.circle(surface, (255, 100, 100), (fruit_x, fruit_y), 2)


def random_food(x, y):
    """Spawn a food item with random size/energy."""
    size = random.randint(*FOOD_SIZE_RANGE)
    energy = random.randint(*FOOD_ENERGY_RANGE)
    return Food(x, y, energy_value=energy, is_carcass=False, size=size)
