"""
Base agent class for all entities in the simulation.
"""
import math
import random
from typing import Dict, Optional, Sequence
import pygame
from simulation.config import SPECIES_STYLE, CLAN_ACCENTS
from simulation.evolution.dna import DNA


class Agent:
    """Base class for all agents in the simulation."""

    _next_id = 1

    def __init__(self, x, y, world_width, world_height, dna: DNA, species: str, clan: Optional[int] = None):
        """
        Initialize an agent with common properties.

        Args:
            x: Initial x position
            y: Initial y position
            world_width: Width of the world
            world_height: Height of the world
            dna: DNA instance
            species: Species name
        """
        self.id = Agent._next_id
        Agent._next_id += 1

        self.x = x
        self.y = y
        self.world_width = world_width
        self.world_height = world_height
        self.dna = dna
        self.species = species
        self.clan = clan if clan is not None else random.randint(0, len(CLAN_ACCENTS) - 1)

        self.energy = 100
        self.max_energy = 160
        self.age = 0
        self.alive = True

        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = random.uniform(0, 2 * math.pi)

        # Cooldowns and metrics
        self.cooldowns: Dict[str, int] = {}
        self.metrics: Dict[str, float] = {
            "kills": 0,
            "survival_time": 0,
            "offspring": 0,
            "energy_gained": 0,
            "stuns": 0,
            "attachments": 0,
        }

    @property
    def speed(self) -> float:
        return self.dna.genes.get("speed", 1.5)

    @property
    def vision(self) -> float:
        return self.dna.genes.get("vision", 80)

    @property
    def size(self) -> float:
        return self.dna.genes.get("size", 4)

    def decay_cooldowns(self):
        """Reduce all cooldown counters."""
        for key in list(self.cooldowns.keys()):
            self.cooldowns[key] = max(0, self.cooldowns[key] - 1)
            if self.cooldowns[key] == 0:
                self.cooldowns.pop(key, None)

    def base_update(self):
        """Common update: age, cooldowns, energy."""
        if not self.alive:
            return False
        self.age += 1
        self.metrics["survival_time"] += 1
        self.decay_cooldowns()
        self.apply_energy_decay(0.3)
        if self.energy <= 0:
            self.alive = False
            return False
        return True

    def move(self):
        """Random wandering with some persistence."""
        if "stunned" in self.cooldowns:
            return
        if random.random() < 0.15:
            self.direction += random.uniform(-0.6, 0.6)
        speed = self.speed * (0.6 if "slowed" in self.cooldowns else 1.0)
        self.velocity_x = math.cos(self.direction) * speed
        self.velocity_y = math.sin(self.direction) * speed
        self.x += self.velocity_x
        self.y += self.velocity_y

    def move_towards(self, target_x, target_y, speed_multiplier=1.0):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.direction = math.atan2(dy, dx)
            speed = self.speed * speed_multiplier
            if "stunned" in self.cooldowns:
                speed = 0
            elif "slowed" in self.cooldowns:
                speed *= 0.6
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
            self.x += self.velocity_x
            self.y += self.velocity_y

    def move_away(self, target_x, target_y, speed_multiplier=1.0):
        dx = self.x - target_x
        dy = self.y - target_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.direction = math.atan2(dy, dx)
            speed = self.speed * speed_multiplier
            if "stunned" in self.cooldowns:
                speed = 0
            elif "slowed" in self.cooldowns:
                speed *= 0.6
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
            self.x += self.velocity_x
            self.y += self.velocity_y

    def distance_to(self, other) -> float:
        if isinstance(other, tuple):
            ox, oy = other
        else:
            ox, oy = other.x, other.y
        dx = self.x - ox
        dy = self.y - oy
        return math.sqrt(dx ** 2 + dy ** 2)

    def find_nearest(self, entities: Sequence, max_distance: Optional[float] = None):
        if not entities:
            return None
        nearest = None
        min_distance = float("inf")
        limit = max_distance or self.vision
        for entity in entities:
            if entity is self or not getattr(entity, "alive", True):
                continue
            distance = self.distance_to(entity)
            if distance < min_distance and distance <= limit:
                min_distance = distance
                nearest = entity
        return nearest

    def apply_energy_decay(self, base_cost: float) -> float:
        """
        Apply an energy tick scaled by size and speed.

        Args:
            base_cost: Baseline energy cost for the agent type
        """
        size_factor = 0.5 + 0.3 * (self.size / 5.0)
        speed_factor = 0.2 * (self.speed / 3.0)
        efficiency = max(0.1, self.dna.genes.get("energy_efficiency", 1.0))
        energy_cost = base_cost * (size_factor + speed_factor) / efficiency
        self.energy -= energy_cost
        return energy_cost

    def clamp_position(self):
        """Keep within bounds."""
        self.x = max(0, min(self.world_width, self.x))
        self.y = max(0, min(self.world_height, self.y))

    def draw(self, surface):
        """Draw agent using its shape/color with a cute face overlay."""
        style = SPECIES_STYLE.get(self.species, {"color": (200, 200, 200), "shape": "circle"})
        base_color = style["color"]
        accent = CLAN_ACCENTS[self.clan % len(CLAN_ACCENTS)]
        color = tuple(int(0.7 * b + 0.3 * a) for b, a in zip(base_color, accent))
        size = int(self.size)
        shape = style["shape"]
        pos = (int(self.x), int(self.y))

        # Soft outline for extra cuteness
        outline_color = tuple(max(0, int(c * 0.8)) for c in color)
        if shape == "triangle":
            points = [
                (pos[0], pos[1] - size),
                (pos[0] - size, pos[1] + size),
                (pos[0] + size, pos[1] + size),
            ]
            pygame.draw.polygon(surface, outline_color, points)
            pygame.draw.polygon(surface, color, points, 0)
        elif shape == "square":
            rect = pygame.Rect(pos[0] - size, pos[1] - size, size * 2, size * 2)
            pygame.draw.rect(surface, outline_color, rect)
            pygame.draw.rect(surface, color, rect.inflate(-2, -2))
        elif shape == "diamond":
            points = [
                (pos[0], pos[1] - size),
                (pos[0] - size, pos[1]),
                (pos[0], pos[1] + size),
                (pos[0] + size, pos[1]),
            ]
            pygame.draw.polygon(surface, outline_color, points)
            pygame.draw.polygon(surface, color, points, 0)
        elif shape == "hex":
            points = [
                (pos[0] + size, pos[1]),
                (pos[0] + size // 2, pos[1] - size),
                (pos[0] - size // 2, pos[1] - size),
                (pos[0] - size, pos[1]),
                (pos[0] - size // 2, pos[1] + size),
                (pos[0] + size // 2, pos[1] + size),
            ]
            pygame.draw.polygon(surface, outline_color, points)
            pygame.draw.polygon(surface, color, points, 0)
        else:
            pygame.draw.circle(surface, outline_color, pos, size + 1)
            pygame.draw.circle(surface, color, pos, size)

        # Tiny face overlay (eyes + smile)
        eye_offset_x = max(2, size // 3)
        eye_offset_y = max(1, size // 4)
        eye_radius = max(1, size // 5)
        eye_color = (255, 255, 255)
        pupil_color = (30, 30, 30)
        left_eye = (pos[0] - eye_offset_x, pos[1] - eye_offset_y)
        right_eye = (pos[0] + eye_offset_x, pos[1] - eye_offset_y)
        pygame.draw.circle(surface, eye_color, left_eye, eye_radius)
        pygame.draw.circle(surface, eye_color, right_eye, eye_radius)
        pygame.draw.circle(surface, pupil_color, left_eye, max(1, eye_radius // 2))
        pygame.draw.circle(surface, pupil_color, right_eye, max(1, eye_radius // 2))

        smile_rect = pygame.Rect(pos[0] - size // 2, pos[1], size, size // 2)
        pygame.draw.arc(surface, pupil_color, smile_rect, math.pi / 10, math.pi - math.pi / 10, 2)
