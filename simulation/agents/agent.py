"""
Base agent class for all entities in the simulation.
"""
import math
import random
from typing import Dict, Optional, Sequence
import pygame
from simulation.config import SPECIES_STYLE, CLAN_ACCENTS
from simulation.evolution.dna import DNA


def draw_gradient_circle(surface, pos, radius, color):
    """Draw a circle with radial gradient for depth."""
    for i in range(radius, 0, -1):
        ratio = i / radius
        # Brighter in center, darker at edges
        grad_color = tuple(min(255, int(c * (0.7 + ratio * 0.3))) for c in color)
        pygame.draw.circle(surface, grad_color, pos, i)


def draw_glow(surface, pos, radius, color, intensity=0.3):
    """Draw a soft glow around an object."""
    glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    glow_color = (*color, int(intensity * 255))
    pygame.draw.circle(glow_surf, glow_color, (radius * 2, radius * 2), radius * 2)
    surface.blit(glow_surf, (pos[0] - radius * 2, pos[1] - radius * 2), special_flags=pygame.BLEND_RGBA_ADD)


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

    @property
    def metabolism(self) -> float:
        """Energy consumption multiplier. Lower is better."""
        return self.dna.genes.get("metabolism", 1.0)

    @property
    def bravery(self) -> float:
        """Likelihood to fight vs flee (0.0 to 1.0)."""
        return self.dna.genes.get("bravery", 0.5)

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
        
        # Idle energy cost
        self.apply_energy_decay(0.3)
        
        if self.energy <= 0:
            self.alive = False
            return False
        return True

    def move(self):
        """Random wandering with some persistence, plus fleeing if scared."""
        if "stunned" in self.cooldowns:
            return

        # Fleeing logic?
        # If low health and low bravery, move erratically or faster
        fleeing = False
        if self.energy < 30 and self.bravery < 0.4:
            fleeing = True

        if random.random() < (0.15 if not fleeing else 0.4):
            change = random.uniform(-0.6, 0.6)
            if fleeing:
                change *= 2.0  # Panic turns
            self.direction += change

        base_speed = self.speed
        if fleeing:
            base_speed *= 1.2  # Adrenaline boost (costs more energy implicitly by distance)
        
        speed = base_speed * (0.6 if "slowed" in self.cooldowns else 1.0)
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
        Apply an energy tick scaled by size, speed, and metabolism.

        Args:
            base_cost: Baseline energy cost for the agent type
        """
        size_factor = 0.5 + 0.3 * (self.size / 5.0)
        speed_factor = 0.2 * (self.speed / 3.0)
        efficiency = max(0.1, self.dna.genes.get("energy_efficiency", 1.0))
        
        # Metabolism multiplier (lower metabolism = lower cost)
        metabolism_factor = self.metabolism
        
        energy_cost = base_cost * (size_factor + speed_factor) * metabolism_factor / efficiency
        self.energy -= energy_cost
        return energy_cost

    def clamp_position(self):
        """Keep within bounds."""
        self.x = max(0, min(self.world_width, self.x))
        self.y = max(0, min(self.world_height, self.y))

    def draw(self, surface):
        """Draw agent with modern visuals, gradients, and cute features."""
        style = SPECIES_STYLE.get(self.species, {"color": (200, 200, 200), "shape": "circle"})
        base_color = style["color"]
        accent = CLAN_ACCENTS[self.clan % len(CLAN_ACCENTS)]
        color = tuple(int(0.7 * b + 0.3 * a) for b, a in zip(base_color, accent))
        size = int(self.size) + 2  # Slightly larger
        shape = style["shape"]
        pos = (int(self.x), int(self.y))

        # Add subtle glow effect
        draw_glow(surface, pos, size + 2, color, intensity=0.15)

        # Shadow for depth
        shadow_offset = 2
        shadow_pos = (pos[0] + shadow_offset, pos[1] + shadow_offset)
        shadow_color = (20, 20, 20)

        if shape == "triangle":
            # Hunter - sharp predator shape
            points = [
                (pos[0], pos[1] - size - 2),
                (pos[0] - size - 1, pos[1] + size),
                (pos[0] + size + 1, pos[1] + size),
            ]
            shadow_points = [
                (shadow_pos[0], shadow_pos[1] - size - 2),
                (shadow_pos[0] - size - 1, shadow_pos[1] + size),
                (shadow_pos[0] + size + 1, shadow_pos[1] + size),
            ]
            pygame.draw.polygon(surface, shadow_color, shadow_points)
            # Gradient effect with layered polygons
            for i in range(3):
                scale = 1 - i * 0.2
                scaled_points = [
                    (pos[0], pos[1] - int((size + 2) * scale)),
                    (pos[0] - int((size + 1) * scale), pos[1] + int(size * scale)),
                    (pos[0] + int((size + 1) * scale), pos[1] + int(size * scale)),
                ]
                grad_color = tuple(min(255, int(c * (0.8 + i * 0.1))) for c in color)
                pygame.draw.polygon(surface, grad_color, scaled_points)

        elif shape == "square":
            # Scavenger - rounded, friendly cube
            shadow_rect = pygame.Rect(shadow_pos[0] - size, shadow_pos[1] - size, size * 2, size * 2)
            pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=size // 2)
            
            # Main body with gradient layers
            for i in range(3):
                shrink = i * 2
                rect = pygame.Rect(pos[0] - size + shrink, pos[1] - size + shrink, size * 2 - shrink * 2, size * 2 - shrink * 2)
                grad_color = tuple(min(255, int(c * (0.75 + i * 0.15))) for c in color)
                pygame.draw.rect(surface, grad_color, rect, border_radius=(size - shrink) // 2)

        elif shape == "diamond":
            # Protector - shield-like diamond
            points = [
                (pos[0], pos[1] - size - 2),
                (pos[0] - size - 2, pos[1]),
                (pos[0], pos[1] + size + 2),
                (pos[0] + size + 2, pos[1]),
            ]
            shadow_points = [(p[0] + shadow_offset, p[1] + shadow_offset) for p in points]
            pygame.draw.polygon(surface, shadow_color, shadow_points)
            
            for i in range(3):
                scale = 1 - i * 0.2
                scaled_points = [
                    (pos[0], pos[1] - int((size + 2) * scale)),
                    (pos[0] - int((size + 2) * scale), pos[1]),
                    (pos[0], pos[1] + int((size + 2) * scale)),
                    (pos[0] + int((size + 2) * scale), pos[1]),
                ]
                grad_color = tuple(min(255, int(c * (0.75 + i * 0.15))) for c in color)
                pygame.draw.polygon(surface, grad_color, scaled_points)

        elif shape == "hex":
            # Parasite - organic hexagon
            angle_offset = math.pi / 6
            points = []
            shadow_points = []
            for i in range(6):
                angle = i * math.pi / 3 + angle_offset
                x = pos[0] + int((size + 2) * math.cos(angle))
                y = pos[1] + int((size + 2) * math.sin(angle))
                points.append((x, y))
                shadow_points.append((x + shadow_offset, y + shadow_offset))
            
            pygame.draw.polygon(surface, shadow_color, shadow_points)
            for i in range(3):
                scale = 1 - i * 0.2
                scaled_points = []
                for j in range(6):
                    angle = j * math.pi / 3 + angle_offset
                    x = pos[0] + int((size + 2) * scale * math.cos(angle))
                    y = pos[1] + int((size + 2) * scale * math.sin(angle))
                    scaled_points.append((x, y))
                grad_color = tuple(min(255, int(c * (0.75 + i * 0.15))) for c in color)
                pygame.draw.polygon(surface, grad_color, scaled_points)

        else:
            # Grazer - soft circle with gradient
            pygame.draw.circle(surface, shadow_color, shadow_pos, size + 2)
            draw_gradient_circle(surface, pos, size + 2, color)

        # Enhanced face features
        eye_offset_x = max(3, size // 2)
        eye_offset_y = max(2, size // 3)
        eye_radius = max(2, size // 3)
        eye_color = (255, 255, 255)
        pupil_color = (30, 30, 30)
        
        left_eye = (pos[0] - eye_offset_x, pos[1] - eye_offset_y)
        right_eye = (pos[0] + eye_offset_x, pos[1] - eye_offset_y)
        
        # Eye whites with shine
        pygame.draw.circle(surface, eye_color, left_eye, eye_radius)
        pygame.draw.circle(surface, eye_color, right_eye, eye_radius)
        
        # Pupils
        pupil_size = max(1, eye_radius // 2)
        pygame.draw.circle(surface, pupil_color, left_eye, pupil_size)
        pygame.draw.circle(surface, pupil_color, right_eye, pupil_size)
        
        # Eye shine
        shine_color = (255, 255, 255, 180)
        pygame.draw.circle(surface, (255, 255, 255), (left_eye[0] - 1, left_eye[1] - 1), max(1, pupil_size // 2))
        pygame.draw.circle(surface, (255, 255, 255), (right_eye[0] - 1, right_eye[1] - 1), max(1, pupil_size // 2))

        # Smile/expression
        frightened = self.energy < 30 and self.bravery < 0.4
        
        if frightened:
            # Worried O mouth
            pygame.draw.circle(surface, pupil_color, (pos[0], pos[1] + size // 2), max(2, size // 3), 2)
        else:
            # Happy smile - thicker and more pronounced
            smile_rect = pygame.Rect(pos[0] - size // 2, pos[1] + size // 4, size, size // 2)
            pygame.draw.arc(surface, pupil_color, smile_rect, math.pi / 10, math.pi - math.pi / 10, 2)
