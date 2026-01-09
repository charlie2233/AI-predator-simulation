"""
World environment for the simulation.
"""
import random
from simulation.agents.prey import Prey
from simulation.agents.predator import Predator
from simulation.agents.food import Food
from simulation.evolution.genetics import EvolutionTracker
from simulation.config import (
    WORLD_WIDTH, WORLD_HEIGHT,
    PREY_INITIAL_COUNT, PREDATOR_INITIAL_COUNT,
    FOOD_COUNT, FOOD_RESPAWN_RATE, MAX_AGENTS
)


class World:
    """The world environment containing all agents and food."""
    
    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT):
        """
        Initialize the world.
        
        Args:
            width: World width
            height: World height
        """
        self.width = width
        self.height = height
        
        self.prey = []
        self.predators = []
        self.food = []
        
        self.generation = 0
        self.time_step = 0
        
        # Evolution tracking
        self.prey_tracker = EvolutionTracker()
        self.predator_tracker = EvolutionTracker()
        
        # Statistics
        self.stats = {
            'prey_born': 0,
            'prey_died': 0,
            'predators_born': 0,
            'predators_died': 0,
            'total_prey': 0,
            'total_predators': 0,
            'total_food': 0
        }
        
        # Initialize population
        self.spawn_initial_population()
    
    def spawn_initial_population(self):
        """Create initial agents and food."""
        # Spawn prey
        for _ in range(PREY_INITIAL_COUNT):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            species = random.choice(['herbivore', 'omnivore'])
            self.prey.append(Prey(x, y, self.width, self.height, species=species))
        
        # Spawn predators
        for _ in range(PREDATOR_INITIAL_COUNT):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            species = random.choice(['carnivore', 'omnivore'])
            self.predators.append(Predator(x, y, self.width, self.height, species=species))
        
        # Spawn food
        for _ in range(FOOD_COUNT):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.food.append(Food(x, y))
    
    def update(self):
        """Update all entities in the world."""
        self.time_step += 1
        
        # Combine all agents for update
        all_agents = self.prey + self.predators
        
        # Update all prey
        for prey in self.prey:
            prey.update(all_agents, self.food)
        
        # Update all predators
        for predator in self.predators:
            predator.update(all_agents, self.food)
        
        # Handle reproduction
        self.handle_reproduction()
        
        # Remove dead entities
        self.remove_dead()
        
        # Respawn food
        self.respawn_food()
        
        # Update statistics
        self.update_stats()
        
        # Record evolution every 100 steps
        if self.time_step % 100 == 0:
            self.prey_tracker.record_generation(self.prey)
            self.predator_tracker.record_generation(self.predators)
    
    def handle_reproduction(self):
        """Handle agent reproduction."""
        new_prey = []
        new_predators = []
        
        # Prey reproduction
        for prey in self.prey:
            if prey.can_reproduce() and len(self.prey) + len(new_prey) < MAX_AGENTS * 0.7:
                # Try to find nearby partner
                partner = None
                for other in self.prey:
                    if other != prey and other.can_reproduce() and prey.distance_to(other) < 50:
                        partner = other
                        break
                
                offspring = prey.reproduce(partner)
                if offspring:
                    new_prey.append(offspring)
                    self.stats['prey_born'] += 1
        
        # Predator reproduction
        for predator in self.predators:
            if predator.can_reproduce() and len(self.predators) + len(new_predators) < MAX_AGENTS * 0.3:
                # Try to find nearby partner
                partner = None
                for other in self.predators:
                    if other != predator and other.can_reproduce() and predator.distance_to(other) < 50:
                        partner = other
                        break
                
                offspring = predator.reproduce(partner)
                if offspring:
                    new_predators.append(offspring)
                    self.stats['predators_born'] += 1
        
        # Add new offspring
        self.prey.extend(new_prey)
        self.predators.extend(new_predators)
    
    def remove_dead(self):
        """Remove dead entities."""
        # Count dead before removal
        dead_prey = sum(1 for p in self.prey if not p.alive)
        dead_predators = sum(1 for p in self.predators if not p.alive)
        
        self.stats['prey_died'] += dead_prey
        self.stats['predators_died'] += dead_predators
        
        # Remove dead
        self.prey = [p for p in self.prey if p.alive]
        self.predators = [p for p in self.predators if p.alive]
        self.food = [f for f in self.food if f.alive]
    
    def respawn_food(self):
        """Randomly respawn food items."""
        if len(self.food) < FOOD_COUNT and random.random() < FOOD_RESPAWN_RATE:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.food.append(Food(x, y))
    
    def update_stats(self):
        """Update current statistics."""
        self.stats['total_prey'] = len(self.prey)
        self.stats['total_predators'] = len(self.predators)
        self.stats['total_food'] = len(self.food)
    
    def get_all_agents(self):
        """Get all agents in the world."""
        return self.prey + self.predators
    
    def reset(self):
        """Reset the world to initial state."""
        self.prey.clear()
        self.predators.clear()
        self.food.clear()
        
        self.generation = 0
        self.time_step = 0
        
        self.prey_tracker = EvolutionTracker()
        self.predator_tracker = EvolutionTracker()
        
        self.stats = {
            'prey_born': 0,
            'prey_died': 0,
            'predators_born': 0,
            'predators_died': 0,
            'total_prey': 0,
            'total_predators': 0,
            'total_food': 0
        }
        
        self.spawn_initial_population()
