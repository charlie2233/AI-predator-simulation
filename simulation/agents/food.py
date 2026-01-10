"""
Food items for the simulation.
"""
import pygame
import random
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

    def draw(self, surface):
        if not self.alive:
            return
        color = FOOD_COLOR if not self.is_carcass else CARCASS_COLOR
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class PlantFood(Food):
    """Larger plant/tree-like food."""

    def __init__(self, x, y, size=None, energy_value=TREE_ENERGY_VALUE):
        size = size if size is not None else random.randint(*TREE_SIZE_RANGE)
        super().__init__(x, y, energy_value=energy_value, is_carcass=False, size=size)

    def draw(self, surface):
        if not self.alive:
            return
        # Draw trunk
        trunk_width = max(2, self.size // 3)
        trunk_height = max(4, self.size)
        trunk_rect = pygame.Rect(int(self.x - trunk_width // 2), int(self.y), trunk_width, trunk_height)
        pygame.draw.rect(surface, (120, 90, 60), trunk_rect)
        # Draw crown
        pygame.draw.circle(surface, FOOD_COLOR, (int(self.x), int(self.y)), self.size)


def random_food(x, y):
    """Spawn a food item with random size/energy."""
    size = random.randint(*FOOD_SIZE_RANGE)
    energy = random.randint(*FOOD_ENERGY_RANGE)
    return Food(x, y, energy_value=energy, is_carcass=False, size=size)
