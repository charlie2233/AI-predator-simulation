"""
Predator agent implementation.
"""
import pygame
import random
from simulation.agents.agent import Agent
from simulation.evolution.genetics import GeneticTraits
from simulation.config import (
    PREDATOR_INITIAL_ENERGY, PREDATOR_MAX_ENERGY,
    PREDATOR_REPRODUCTION_ENERGY, PREDATOR_REPRODUCTION_COST,
    PREDATOR_HUNT_ENERGY_GAIN, RED
)


class Predator(Agent):
    """Predator agent that hunts prey."""
    
    def __init__(self, x, y, world_width, world_height, traits=None, species='carnivore'):
        """
        Initialize predator agent.
        
        Args:
            x: Initial x position
            y: Initial y position
            world_width: Width of the world
            world_height: Height of the world
            traits: GeneticTraits instance
            species: Species type ('carnivore', 'omnivore')
        """
        super().__init__(x, y, world_width, world_height, traits)
        
        self.energy = PREDATOR_INITIAL_ENERGY
        self.max_energy = PREDATOR_MAX_ENERGY
        self.reproduction_cooldown = 150
        self.species = species
        self.hunt_success_count = 0
        
        # Species-specific colors
        if species == 'carnivore':
            self.color = (200, 50, 50)
        elif species == 'omnivore':
            self.color = (200, 100, 200)
        else:
            self.color = RED
    
    def update(self, agents, food_items):
        """
        Update predator behavior.
        
        Args:
            agents: List of all agents
            food_items: List of food items
        """
        if not self.alive:
            return
        
        self.age += 1
        self.reproduction_timer += 1
        
        # Energy decay (predators use more energy)
        self.apply_energy_decay(0.5)
        
        if self.energy <= 0:
            self.alive = False
            return
        
        # Find prey (import here to avoid circular import at module level)
        from simulation.agents.prey import Prey
        prey_list = [a for a in agents if isinstance(a, Prey) and a.alive]
        nearest_prey = self.find_nearest(prey_list)
        
        # Hunt behavior
        if nearest_prey:
            # Chase prey
            self.move_towards(nearest_prey.x, nearest_prey.y, speed_multiplier=1.2)
            
            # Attack if close enough
            if self.distance_to(nearest_prey) < self.traits.size + nearest_prey.traits.size:
                # Successful hunt
                self.energy = min(self.max_energy, self.energy + PREDATOR_HUNT_ENERGY_GAIN)
                nearest_prey.alive = False
                self.hunt_success_count += 1
        else:
            # Random wandering when no prey is visible
            self.move()
        
        # Keep within bounds
        self.x = max(0, min(self.world_width, self.x))
        self.y = max(0, min(self.world_height, self.y))
    
    def can_reproduce(self):
        """Check if predator can reproduce."""
        return (self.alive and 
                self.energy > PREDATOR_REPRODUCTION_ENERGY and 
                self.reproduction_timer > self.reproduction_cooldown)
    
    def reproduce(self, partner=None):
        """
        Create offspring predator.
        
        Args:
            partner: Another predator for reproduction
            
        Returns:
            New Predator instance or None
        """
        if not self.can_reproduce():
            return None
        
        # Create offspring traits
        if partner and isinstance(partner, Predator) and partner.can_reproduce():
            offspring_traits = self.traits.crossover(partner.traits)
            self.energy -= PREDATOR_REPRODUCTION_COST
            partner.energy -= PREDATOR_REPRODUCTION_COST
        else:
            offspring_traits = self.traits.copy()
            offspring_traits.mutate()
            self.energy -= PREDATOR_REPRODUCTION_COST
        
        self.reproduction_timer = 0
        
        # Create offspring
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        
        return Predator(
            self.x + offset_x,
            self.y + offset_y,
            self.world_width,
            self.world_height,
            offspring_traits,
            self.species
        )
    
    def draw(self, surface):
        """
        Draw the predator agent.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self.alive:
            return
        
        # Color intensity based on energy
        energy_ratio = self.energy / self.max_energy
        base_color = self.color
        color = tuple(int(c * (0.5 + 0.5 * energy_ratio)) for c in base_color)
        
        # Size based on traits (predators are larger)
        size = int(self.traits.size) + 2
        
        # Draw as triangle for distinction
        points = [
            (int(self.x), int(self.y - size)),
            (int(self.x - size), int(self.y + size)),
            (int(self.x + size), int(self.y + size))
        ]
        pygame.draw.polygon(surface, color, points)
