"""
Food items for the simulation.
"""
import pygame
import random
from simulation.config import FOOD_SIZE, FOOD_ENERGY_VALUE, FOOD_COLOR, CARCASS_COLOR

class Food:
    """Food item (plant or carcass)."""
    
    def __init__(self, x, y, energy_value=FOOD_ENERGY_VALUE, is_carcass=False):
        """
        Initialize food item.
        
        Args:
            x: X position
            y: Y position
            energy_value: Energy to grant
            is_carcass: Whether this is a carcass drop
        """
        self.x = x
        self.y = y
        self.alive = True
        self.energy_value = energy_value
        self.size = FOOD_SIZE
        self.is_carcass = is_carcass
    
    def draw(self, surface):
        """
        Draw the food item.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self.alive:
            return
        
        color = FOOD_COLOR if not self.is_carcass else CARCASS_COLOR
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
