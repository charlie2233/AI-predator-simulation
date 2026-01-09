"""
Non-living world elements like rocks and shelters.
"""
import pygame
from simulation.config import SHELTER_RADIUS, LIGHT_GRAY, DARK_GRAY


class Rock:
    """Resource node that can be converted into a shelter."""

    def __init__(self, x, y, size=6):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True

    def draw(self, surface):
        if not self.alive:
            return
        color = (120, 110, 100)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)


class Shelter:
    """Shelter that gives nearby agents disaster protection."""

    def __init__(self, x, y, radius=SHELTER_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius
        self.alive = True

    def draw(self, surface):
        if not self.alive:
            return
        pygame.draw.circle(surface, DARK_GRAY, (int(self.x), int(self.y)), self.radius, 2)
        pygame.draw.circle(surface, LIGHT_GRAY, (int(self.x), int(self.y)), self.radius // 3, 0)
