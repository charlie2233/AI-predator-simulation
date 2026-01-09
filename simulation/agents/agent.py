"""
Base agent class for all entities in the simulation.
"""
import math
import random
import pygame
from simulation.evolution.genetics import GeneticTraits


class Agent:
    """Base class for all agents in the simulation."""
    
    def __init__(self, x, y, world_width, world_height, traits=None):
        """
        Initialize an agent.
        
        Args:
            x: Initial x position
            y: Initial y position
            world_width: Width of the world
            world_height: Height of the world
            traits: GeneticTraits instance (creates new if None)
        """
        self.x = x
        self.y = y
        self.world_width = world_width
        self.world_height = world_height
        
        self.traits = traits if traits else GeneticTraits()
        
        self.energy = 100
        self.max_energy = 150
        self.age = 0
        self.alive = True
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = random.uniform(0, 2 * math.pi)
        
        # Reproduction
        self.reproduction_cooldown = 0
        self.reproduction_timer = 0
        
    def update(self, agents, food_items):
        """
        Update agent state.
        
        Args:
            agents: List of all agents
            food_items: List of food items
        """
        if not self.alive:
            return
        
        self.age += 1
        self.reproduction_timer += 1
        
        # Decay energy
        energy_cost = 0.3 / self.traits.energy_efficiency
        self.energy -= energy_cost
        
        # Die if out of energy
        if self.energy <= 0:
            self.alive = False
            return
        
        # Move
        self.move()
        
        # Keep within bounds
        self.x = max(0, min(self.world_width, self.x))
        self.y = max(0, min(self.world_height, self.y))
    
    def move(self):
        """Update position based on velocity."""
        # Random wandering with some momentum
        if random.random() < 0.1:
            self.direction += random.uniform(-0.5, 0.5)
        
        speed = self.traits.speed
        self.velocity_x = math.cos(self.direction) * speed
        self.velocity_y = math.sin(self.direction) * speed
        
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def move_towards(self, target_x, target_y, speed_multiplier=1.0):
        """
        Move towards a target position.
        
        Args:
            target_x: Target x coordinate
            target_y: Target y coordinate
            speed_multiplier: Speed adjustment factor
        """
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.direction = math.atan2(dy, dx)
            speed = self.traits.speed * speed_multiplier
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
            
            self.x += self.velocity_x
            self.y += self.velocity_y
    
    def move_away(self, target_x, target_y, speed_multiplier=1.0):
        """
        Move away from a target position.
        
        Args:
            target_x: Target x coordinate
            target_y: Target y coordinate
            speed_multiplier: Speed adjustment factor
        """
        dx = self.x - target_x
        dy = self.y - target_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.direction = math.atan2(dy, dx)
            speed = self.traits.speed * speed_multiplier
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
            
            self.x += self.velocity_x
            self.y += self.velocity_y
    
    def distance_to(self, other):
        """
        Calculate distance to another agent or position.
        
        Args:
            other: Another agent or (x, y) tuple
            
        Returns:
            Distance value
        """
        if isinstance(other, tuple):
            ox, oy = other
        else:
            ox, oy = other.x, other.y
        
        dx = self.x - ox
        dy = self.y - oy
        return math.sqrt(dx**2 + dy**2)
    
    def find_nearest(self, entities):
        """
        Find nearest entity from a list.
        
        Args:
            entities: List of entities to search
            
        Returns:
            Nearest entity or None
        """
        if not entities:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for entity in entities:
            if entity is self or not getattr(entity, 'alive', True):
                continue
            
            distance = self.distance_to(entity)
            if distance < min_distance and distance <= self.traits.vision:
                min_distance = distance
                nearest = entity
        
        return nearest
    
    def can_reproduce(self):
        """Check if agent can reproduce."""
        return (self.alive and 
                self.energy > self.max_energy * 0.8 and 
                self.reproduction_timer > self.reproduction_cooldown)
    
    def reproduce(self, partner=None):
        """
        Create offspring.
        
        Args:
            partner: Another agent for sexual reproduction (None for asexual)
            
        Returns:
            New agent instance or None
        """
        if not self.can_reproduce():
            return None
        
        # Create offspring traits
        if partner and partner.can_reproduce():
            # Sexual reproduction
            offspring_traits = self.traits.crossover(partner.traits)
            self.energy -= self.max_energy * 0.4
            partner.energy -= partner.max_energy * 0.4
        else:
            # Asexual reproduction
            offspring_traits = self.traits.copy()
            offspring_traits.mutate()
            self.energy -= self.max_energy * 0.4
        
        # Reset reproduction timer
        self.reproduction_timer = 0
        
        # Create offspring near parent
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        
        return self.__class__(
            self.x + offset_x,
            self.y + offset_y,
            self.world_width,
            self.world_height,
            offspring_traits
        )
    
    def draw(self, surface):
        """
        Draw the agent.
        
        Args:
            surface: Pygame surface to draw on
        """
        pass  # Implemented by subclasses
