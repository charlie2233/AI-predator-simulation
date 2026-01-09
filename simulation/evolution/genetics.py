"""
Genetic traits and evolution system for agents.
"""
import random
import copy
from simulation.config import (
    MUTATION_RATE, MUTATION_STRENGTH,
    TRAIT_MIN_VALUES, TRAIT_MAX_VALUES
)


class GeneticTraits:
    """Represents the genetic traits of an agent."""
    
    def __init__(self, speed=None, vision=None, energy_efficiency=None, size=None):
        """
        Initialize genetic traits.
        
        Args:
            speed: Movement speed multiplier
            vision: Vision range for detecting other agents
            energy_efficiency: How efficiently energy is used
            size: Physical size of the agent
        """
        self.speed = speed if speed is not None else random.uniform(1.0, 3.0)
        self.vision = vision if vision is not None else random.uniform(50, 100)
        self.energy_efficiency = energy_efficiency if energy_efficiency is not None else random.uniform(0.8, 1.2)
        self.size = size if size is not None else random.uniform(3, 7)
        
    def mutate(self):
        """Apply random mutations to traits."""
        traits = ['speed', 'vision', 'energy_efficiency', 'size']
        
        for trait in traits:
            if random.random() < MUTATION_RATE:
                current_value = getattr(self, trait)
                mutation = random.gauss(0, MUTATION_STRENGTH) * current_value
                new_value = current_value + mutation
                
                # Clamp to min/max values
                min_val = TRAIT_MIN_VALUES.get(trait, 0.1)
                max_val = TRAIT_MAX_VALUES.get(trait, 10.0)
                new_value = max(min_val, min(max_val, new_value))
                
                setattr(self, trait, new_value)
    
    def crossover(self, other: 'GeneticTraits') -> 'GeneticTraits':
        """
        Create offspring traits by combining with another parent.
        
        Args:
            other: Another GeneticTraits instance
            
        Returns:
            New GeneticTraits instance
        """
        offspring = GeneticTraits()
        
        # Each trait has 50% chance of coming from either parent
        offspring.speed = self.speed if random.random() < 0.5 else other.speed
        offspring.vision = self.vision if random.random() < 0.5 else other.vision
        offspring.energy_efficiency = self.energy_efficiency if random.random() < 0.5 else other.energy_efficiency
        offspring.size = self.size if random.random() < 0.5 else other.size
        
        # Apply mutation
        offspring.mutate()
        
        return offspring
    
    def copy(self):
        """Create a copy of these traits."""
        return GeneticTraits(
            speed=self.speed,
            vision=self.vision,
            energy_efficiency=self.energy_efficiency,
            size=self.size
        )
    
    def get_fitness_score(self):
        """Calculate overall fitness score based on traits."""
        # Balanced traits are generally better
        return (self.speed * 0.3 + 
                self.vision * 0.002 + 
                self.energy_efficiency * 10 + 
                self.size * 0.5)
    
    def to_dict(self):
        """Convert traits to dictionary."""
        return {
            'speed': self.speed,
            'vision': self.vision,
            'energy_efficiency': self.energy_efficiency,
            'size': self.size
        }


class EvolutionTracker:
    """Tracks evolution statistics over generations."""
    
    def __init__(self):
        """Initialize evolution tracker."""
        self.generation = 0
        self.trait_history = {
            'speed': [],
            'vision': [],
            'energy_efficiency': [],
            'size': []
        }
        self.population_history = []
        self.fitness_history = []
    
    def record_generation(self, agents):
        """
        Record statistics for the current generation.
        
        Args:
            agents: List of agents to analyze
        """
        if not agents:
            return
        
        self.generation += 1
        
        # Calculate average traits
        avg_traits = {
            'speed': sum(a.traits.speed for a in agents) / len(agents),
            'vision': sum(a.traits.vision for a in agents) / len(agents),
            'energy_efficiency': sum(a.traits.energy_efficiency for a in agents) / len(agents),
            'size': sum(a.traits.size for a in agents) / len(agents)
        }
        
        for trait, value in avg_traits.items():
            self.trait_history[trait].append(value)
        
        self.population_history.append(len(agents))
        
        # Calculate average fitness
        avg_fitness = sum(a.traits.get_fitness_score() for a in agents) / len(agents)
        self.fitness_history.append(avg_fitness)
    
    def get_recent_history(self, window=100):
        """
        Get recent history for visualization.
        
        Args:
            window: Number of recent generations to return
            
        Returns:
            Dictionary of recent trait history
        """
        return {
            trait: values[-window:] 
            for trait, values in self.trait_history.items()
        }
