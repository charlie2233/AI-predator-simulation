"""
World environment and generational evolution.
"""
import random
from typing import Dict, List, Tuple

from simulation.agents.food import Food
from simulation.agents.terrain import Rock, Shelter
from simulation.evolution.dna import DNA
from simulation.evolution.evolution import Archive, reproduce, tournament_selection
from simulation.species import Grazer, Hunter, Scavenger, Protector, Parasite
from simulation.stats import StatsLogger
from simulation.config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    FOOD_COUNT,
    FOOD_RESPAWN_RATE,
    CARCASS_ENERGY_VALUE,
    EPISODE_LENGTH_STEPS,
    SPECIES_DNA_RANGES,
    INITIAL_SPECIES_COUNTS,
    RANDOM_SEED,
    OBSTACLES_ENABLED,
    OBSTACLE_COUNT,
    OBSTACLE_RADIUS,
    MUTATION_SIGMA,
    ROCK_COUNT,
    ROCK_RESPAWN_RATE,
    SHELTER_RADIUS,
    EVENT_PROBABILITIES,
    EVENT_SEVERITY,
    MAX_EVENT_CASUALTY_FRACTION,
)


SPECIES_CLASS = {
    "grazer": Grazer,
    "hunter": Hunter,
    "scavenger": Scavenger,
    "protector": Protector,
    "parasite": Parasite,
}


class World:
    """The world environment containing all agents and food."""

    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT, config_overrides=None):
        config_overrides = config_overrides or {}
        self.width = config_overrides.get("world_width", width)
        self.height = config_overrides.get("world_height", height)
        self.episode_length = config_overrides.get("episode_length", EPISODE_LENGTH_STEPS)
        self.food_respawn_rate = config_overrides.get("food_respawn_rate", FOOD_RESPAWN_RATE)
        self.mutation_sigma = config_overrides.get("mutation_sigma", MUTATION_SIGMA)
        self.obstacles_enabled = config_overrides.get("obstacles_enabled", OBSTACLES_ENABLED)
        self.initial_counts = dict(INITIAL_SPECIES_COUNTS)
        self.initial_counts.update(config_overrides.get("initial_counts", {}))

        random.seed(RANDOM_SEED)

        self.populations: Dict[str, List] = {name: [] for name in SPECIES_CLASS.keys()}
        self.food: List[Food] = []
        self.rocks: List[Rock] = []
        self.shelters: List[Shelter] = []
        self.obstacles: List[Tuple[float, float]] = []
        self.archive = Archive()
        self.stats = StatsLogger()

        self.generation = 1
        self.episode_step = 0
        self.extinction_log: List[str] = []

        self.spawn_initial_population()

    def spawn_initial_population(self):
        """Create initial agents and food."""
        self.populations = {name: [] for name in SPECIES_CLASS.keys()}
        for species, count in self.initial_counts.items():
            for _ in range(count):
                self.populations[species].append(self._make_agent(species))

        self.food = []
        for _ in range(FOOD_COUNT):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.food.append(Food(x, y))

        self.rocks = []
        for _ in range(ROCK_COUNT):
            self.rocks.append(Rock(random.uniform(0, self.width), random.uniform(0, self.height)))

        self.obstacles = []
        if self.obstacles_enabled:
            for _ in range(OBSTACLE_COUNT):
                self.obstacles.append(
                    (random.uniform(OBSTACLE_RADIUS, self.width - OBSTACLE_RADIUS), random.uniform(OBSTACLE_RADIUS, self.height - OBSTACLE_RADIUS))
                )

    def _make_agent(self, species: str, dna: DNA = None):
        klass = SPECIES_CLASS[species]
        dna_ranges = SPECIES_DNA_RANGES[species]
        if dna is None:
            genes = {k: random.uniform(low, high) for k, (low, high) in dna_ranges.items()}
            dna = DNA(genes, dna_ranges)
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        clan = random.randint(0, 2)
        return klass(x, y, self.width, self.height, dna, species=species, clan=clan)

    def update(self):
        """Update all entities in the world."""
        self.episode_step += 1

        context = {
            "food": self.food,
            "populations": self.populations,
            "obstacles": self.obstacles,
            "rocks": self.rocks,
            "shelters": self.shelters,
            "build_shelter": self.build_shelter,
        }

        for species, agents in self.populations.items():
            for agent in list(agents):
                if agent.alive:
                    agent.update(context)
                    self._apply_obstacle_avoidance(agent)
                else:
                    # Drop carcass
                    if random.random() < 0.6:
                        self.food.append(Food(agent.x, agent.y, energy_value=CARCASS_ENERGY_VALUE, is_carcass=True))

        self._remove_dead()
        self._respawn_food()
        self._respawn_rocks()
        self._maybe_trigger_event()

        if self.episode_step >= self.episode_length:
            self.end_episode()

    def _apply_obstacle_avoidance(self, agent):
        """Push agents away from obstacles."""
        if not self.obstacles_enabled:
            agent.clamp_position()
            return
        for (ox, oy) in self.obstacles:
            dx = agent.x - ox
            dy = agent.y - oy
            dist_sq = dx * dx + dy * dy
            if dist_sq < OBSTACLE_RADIUS ** 2 and dist_sq > 0:
                agent.move_away(ox, oy, speed_multiplier=1.2)
        agent.clamp_position()

    def _respawn_food(self):
        """Randomly respawn food items."""
        if len(self.food) < FOOD_COUNT and random.random() < self.food_respawn_rate:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.food.append(Food(x, y))

    def _respawn_rocks(self):
        if len(self.rocks) < ROCK_COUNT and random.random() < ROCK_RESPAWN_RATE:
            self.rocks.append(Rock(random.uniform(0, self.width), random.uniform(0, self.height)))

    def _remove_dead(self):
        """Remove dead entities and ensure non-negative counts."""
        for key in list(self.populations.keys()):
            self.populations[key] = [a for a in self.populations[key] if a.alive]
            if len(self.populations[key]) < 0:
                self.populations[key] = []

        self.food = [f for f in self.food if f.alive]
        self.rocks = [r for r in self.rocks if getattr(r, "alive", True)]
        self.shelters = [s for s in self.shelters if getattr(s, "alive", True)]

    def _maybe_trigger_event(self):
        """Random disasters to shake dynamics without wiping species."""
        for event_type, prob in EVENT_PROBABILITIES.items():
            if random.random() < prob:
                self._apply_event(event_type)

    def _apply_event(self, event_type: str, center: Tuple[float, float] = None, radius: float = None):
        severity = EVENT_SEVERITY.get(event_type, 1.0)
        max_casualties = {sp: max(1, int(len(agents) * MAX_EVENT_CASUALTY_FRACTION)) for sp, agents in self.populations.items()}
        casualties = {sp: 0 for sp in self.populations.keys()}
        shelters = self.shelters
        radius = radius or max(self.width, self.height)  # global if none

        for species, agents in self.populations.items():
            for agent in agents:
                if casualties[species] >= max_casualties[species]:
                    continue
                if center:
                    if agent.distance_to(center) > radius:
                        continue
                sheltered = any(agent.distance_to(sh) < sh.radius for sh in shelters)
                if sheltered:
                    continue
                agent.energy -= 15 * severity
                if event_type == 'meteor':
                    agent.energy -= 10 * severity
                if agent.energy <= 0 and random.random() < 0.6:
                    agent.alive = False
                    casualties[species] += 1

        loc_text = f" at {center}" if center else ""
        self.extinction_log.append(f"Gen {self.generation} event: {event_type}{loc_text} (sev {severity:.1f})")

    def build_shelter(self, rock: Rock, builder=None):
        """Convert rock into shelter."""
        if not getattr(rock, "alive", True):
            return
        rock.alive = False
        self.shelters.append(Shelter(rock.x, rock.y, radius=SHELTER_RADIUS))
        name = builder.species if builder else "agent"
        self.extinction_log.append(f"Gen {self.generation}: {name} built shelter")

    def apply_manual_event(self, event_type: str, position: Tuple[float, float], radius: float = 140):
        """Trigger a targeted event at a world position."""
        self._apply_event(event_type, center=position, radius=radius)

    def end_episode(self):
        """Compute fitness, evolve populations, log stats."""
        scored_per_species: Dict[str, List[tuple]] = {}
        mean_dna: Dict[str, Dict[str, float]] = {}
        extinctions: List[str] = []

        for species, agents in self.populations.items():
            klass = SPECIES_CLASS[species]
            scored = []
            if agents:
                for agent in agents:
                    fitness = klass.fitness(agent)
                    scored.append((fitness, agent.dna))
                scored_per_species[species] = scored
                # Mean dna
                if scored:
                    mean_dna[species] = {
                        gene: sum(a.dna.genes[gene] for a in agents) / len(agents) for gene in agents[0].dna.genes.keys()
                    }
            else:
                extinctions.append(species)
                scored_per_species[species] = []
                mean_dna[species] = {gene: 0 for gene in SPECIES_DNA_RANGES[species].keys()}

            # Archive update
            self.archive.add_generation(species, scored)

        # Record stats
        counts = {species: len(agents) for species, agents in self.populations.items()}
        self.stats.record(self.generation, counts, mean_dna, extinctions)
        if extinctions:
            self.extinction_log.extend([f"Gen {self.generation}: {sp} extinct" for sp in extinctions])

        # Build next generation
        new_populations: Dict[str, List] = {name: [] for name in SPECIES_CLASS.keys()}
        for species, target_count in self.initial_counts.items():
            scored = scored_per_species.get(species, [])
            selected = tournament_selection(scored, max(2, target_count // 2))
            children_dna = reproduce(selected, target_count, sigma=self.mutation_sigma)

            # Extinction recovery
            if not children_dna:
                archived = self.archive.sample(species, target_count, sigma_boost=2.0)
                if archived:
                    children_dna = archived
            if not children_dna:
                # Fallback random
                children_dna = [self._random_dna(species) for _ in range(target_count)]

            new_populations[species] = [self._make_agent(species, dna) for dna in children_dna]

        self.populations = new_populations
        self.food = []
        for _ in range(FOOD_COUNT):
            self.food.append(Food(random.uniform(0, self.width), random.uniform(0, self.height)))

        self.episode_step = 0
        self.generation += 1

    def _random_dna(self, species: str) -> DNA:
        ranges = SPECIES_DNA_RANGES[species]
        genes = {k: random.uniform(low, high) for k, (low, high) in ranges.items()}
        return DNA(genes, ranges)

    def reset_generation(self):
        """End episode early and restart."""
        self.end_episode()

    def reset_all(self, config_overrides=None):
        """Reset world and archive."""
        config_overrides = config_overrides or {}
        self.__init__(self.width, self.height, config_overrides)
        self.archive = Archive()
        self.stats = StatsLogger()
        self.generation = 1
        self.episode_step = 0

    def get_all_agents(self):
        """Get all agents in the world."""
        result = []
        for agents in self.populations.values():
            result.extend(agents)
        return result
