"""
Prey agent implementation.
"""
import pygame
import random
from typing import TYPE_CHECKING
from simulation.agents.agent import Agent
from simulation.evolution.genetics import GeneticTraits
from simulation.config import (
    PREY_INITIAL_ENERGY, PREY_MAX_ENERGY,
    PREY_REPRODUCTION_ENERGY, PREY_REPRODUCTION_COST,
    GREEN, YELLOW
)

if TYPE_CHECKING:
    from simulation.agents.predator import Predator


class Prey(Agent):
    """Prey agent that eats food and avoids predators."""
    
    def __init__(self, x, y, world_width, world_height, traits=None, species='herbivore'):
        """
        Initialize prey agent.
        
        Args:
            x: Initial x position
            y: Initial y position
            world_width: Width of the world
            world_height: Height of the world
            traits: GeneticTraits instance
            species: Species type ('herbivore', 'omnivore')
        """
        super().__init__(x, y, world_width, world_height, traits)
        
        self.energy = PREY_INITIAL_ENERGY
        self.max_energy = PREY_MAX_ENERGY
        self.reproduction_cooldown = 100
        self.species = species
        
        # Species-specific colors
        if species == 'herbivore':
            self.color = (50, 200, 50)
        elif species == 'omnivore':
            self.color = (200, 200, 50)
        else:
            self.color = GREEN
    
    def update(self, agents, food_items):
        """
        Update prey behavior.
        
        Args:
            agents: List of all agents
            food_items: List of food items
        """
        if not self.alive:
            return
        
        self.age += 1
        self.reproduction_timer += 1
        
        # Energy decay based on traits
        self.apply_energy_decay(0.3)
        
        if self.energy <= 0:
            self.alive = False
            return
        
        # Find predators and food
        from simulation.agents.predator import Predator  # Import here to avoid circular dependency
        predators = [a for a in agents if isinstance(a, Predator) and a.alive]
        nearest_predator = self.find_nearest(predators)
        nearest_food = self.find_nearest(food_items)
        
        # Behavior priority: avoid predators > find food > wander
        if nearest_predator and self.distance_to(nearest_predator) < self.traits.vision * 0.7:
            # Flee from predator
            self.move_away(nearest_predator.x, nearest_predator.y, speed_multiplier=1.5)
        elif nearest_food:
            # Move towards food
            self.move_towards(nearest_food.x, nearest_food.y)
            
            # Eat if close enough
            if self.distance_to(nearest_food) < self.traits.size + 5:
                self.energy = min(self.max_energy, self.energy + nearest_food.energy_value)
                nearest_food.alive = False
        else:
            # Random wandering
            self.move()
        
        # Keep within bounds
        self.x = max(0, min(self.world_width, self.x))
        self.y = max(0, min(self.world_height, self.y))
    
    def can_reproduce(self):
        """Check if prey can reproduce."""
        return (self.alive and 
                self.energy > PREY_REPRODUCTION_ENERGY and 
                self.reproduction_timer > self.reproduction_cooldown)
    
    def reproduce(self, partner=None):
        """
        Create offspring prey.
        
        Args:
            partner: Another prey for reproduction
            
        Returns:
            New Prey instance or None
        """
        if not self.can_reproduce():
            return None
        
        # Create offspring traits
        if partner and isinstance(partner, Prey) and partner.can_reproduce():
            offspring_traits = self.traits.crossover(partner.traits)
            self.energy -= PREY_REPRODUCTION_COST
            partner.energy -= PREY_REPRODUCTION_COST
        else:
            offspring_traits = self.traits.copy()
            offspring_traits.mutate()
            self.energy -= PREY_REPRODUCTION_COST
        
        self.reproduction_timer = 0
        
        # Create offspring
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        
        return Prey(
            self.x + offset_x,
            self.y + offset_y,
            self.world_width,
            self.world_height,
            offspring_traits,
            self.species
        )
    
    def draw(self, surface):
        """
        Draw the prey agent.
        
        Args:
            surface: Pygame surface to draw on
        """
        if not self.alive:
            return
        
        # Color intensity based on energy
        energy_ratio = self.energy / self.max_energy
        base_color = self.color
        color = tuple(int(c * (0.5 + 0.5 * energy_ratio)) for c in base_color)
        
        # Size based on traits
        size = int(self.traits.size)
        
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
        
        # Draw vision range (for debugging, can be toggled)
        # pygame.draw.circle(surface, (*color, 50), (int(self.x), int(self.y)), int(self.traits.vision), 1)
