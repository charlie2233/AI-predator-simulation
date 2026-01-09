"""
Food items for the simulation.
"""
import pygame
import random
from simulation.config import FOOD_SIZE, FOOD_ENERGY_VALUE, GREEN


class Food:
    """Food item that prey can consume."""
    
    def __init__(self, x, y):
        """
        Initialize food item.
        
        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.alive = True
        self.energy_value = FOOD_ENERGY_VALUE
        self.size = FOOD_SIZE
    
    def draw(self, surface):
        """
        Draw the food item.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self.alive:
            return
        
        color = (100, 255, 100)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)
