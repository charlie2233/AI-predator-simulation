"""
World environment and generational evolution.
"""
import random
from typing import Dict, List, Tuple

from simulation.agents.food import Food, PlantFood, random_food
from simulation.agents.terrain import Rock, Shelter
from simulation.evolution.dna import DNA
from simulation.evolution.evolution import Archive, reproduce, tournament_selection
from simulation.species import Grazer, Hunter, Scavenger, Protector, Parasite, Apex, SeaHunter
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
    TREE_COUNT,
    WATER_ZONE_COUNT,
    WATER_ZONE_WIDTH,
    WATER_ZONE_HEIGHT,
    WATER_BLOOM_RATE,
    DISASTER_RADIUS,
    SEA_COLOR,
    RIVER_COLOR,
    CLAN_TRAITS,
)


SPECIES_CLASS = {
    "grazer": Grazer,
    "hunter": Hunter,
    "scavenger": Scavenger,
    "protector": Protector,
    "parasite": Parasite,
    "apex": Apex,
    "sea_hunter": SeaHunter,
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
        self.water_zones: List[Tuple[float, float, float, float, str]] = []  # x, y, w, h, type
        self.obstacles: List[Tuple[float, float]] = []
        self.archive = Archive()
        self.stats = StatsLogger()

        self.generation = 1
        self.episode_step = 0
        self.extinction_log: List[str] = []
        
        # New stats / visual state
        self.run_history = {
            "starts": 1,
            "extinctions": 0,
            "manual_resets": 0
        }
        self.active_event_text = None
        self.active_event_timer = 0

        self._generate_water_zones()
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
            self.food.append(random_food(x, y))
        for _ in range(TREE_COUNT):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.food.append(PlantFood(x, y))

        self.rocks = []
        for _ in range(ROCK_COUNT):
            self.rocks.append(Rock(random.uniform(0, self.width), random.uniform(0, self.height)))

        self.obstacles = []
        if self.obstacles_enabled:
            for _ in range(OBSTACLE_COUNT):
                self.obstacles.append(
                    (random.uniform(OBSTACLE_RADIUS, self.width - OBSTACLE_RADIUS), random.uniform(OBSTACLE_RADIUS, self.height - OBSTACLE_RADIUS))
                )

    def _generate_water_zones(self):
        """Create simple vertical water/river bands."""
        self.water_zones = []
        band_width = WATER_ZONE_WIDTH
        for i in range(WATER_ZONE_COUNT):
            # Evenly spaced random offsets
            base_x = (i + 1) * self.width / (WATER_ZONE_COUNT + 1)
            jitter = random.uniform(-band_width * 0.5, band_width * 0.5)
            x = max(0, min(self.width - band_width, base_x + jitter))
            zone_type = "sea" if i == 0 else "river"
            self.water_zones.append((x, 0, band_width, WATER_ZONE_HEIGHT, zone_type))

    def _make_agent(self, species: str, dna: DNA = None):
        klass = SPECIES_CLASS[species]
        dna_ranges = SPECIES_DNA_RANGES[species]
        if dna is None:
            genes = {k: random.uniform(low, high) for k, (low, high) in dna_ranges.items()}
            dna = DNA(genes, dna_ranges)
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        clan = random.randint(0, len(CLAN_TRAITS) - 1)
        # Apply clan multipliers to DNA for diversity
        clan_mod = CLAN_TRAITS[clan]
        for key, mult in clan_mod.items():
            if key in dna.genes:
                dna.genes[key] *= mult
        return klass(x, y, self.width, self.height, dna, species=species, clan=clan)

    def update(self):
        """Update all entities in the world."""
        self.episode_step += 1
        
        if self.active_event_timer > 0:
            self.active_event_timer -= 1
            if self.active_event_timer <= 0:
                self.active_event_text = None

        context = {
            "food": self.food,
            "populations": self.populations,
            "obstacles": self.obstacles,
            "rocks": self.rocks,
            "shelters": self.shelters,
            "build_shelter": self.build_shelter,
            "is_in_water": self._point_in_water,
            "nearest_water_point": self._nearest_water_point,
            "nearest_land_point": self._nearest_land_point,
        }

        for species, agents in self.populations.items():
            for agent in list(agents):
                if agent.alive:
                    agent.update(context)
                    self._push_rocks(agent)
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
            self.food.append(random_food(x, y))
        if len(self.food) < FOOD_COUNT and self.water_zones and random.random() < WATER_BLOOM_RATE:
            wx, wy = self._random_water_point()
            self.food.append(PlantFood(wx, wy))

    def _push_rocks(self, agent):
        """Allow agents to nudge rocks, making the world feel more interactive."""
        if not self.rocks:
            return
        capacity = agent.dna.genes.get("carry_capacity", 8)
        rock_skill = agent.dna.genes.get("rock_skill", 1.0)
        for rock in self.rocks:
            if not getattr(rock, "alive", True):
                continue
            dist = agent.distance_to(rock)
            if dist < rock.size + agent.size + 2:
                # Nudge rock in agent's facing direction
                dx = agent.velocity_x
                dy = agent.velocity_y
                step = capacity * 0.08 * rock_skill
                rock.x = max(0, min(self.width, rock.x + dx * step))
                rock.y = max(0, min(self.height, rock.y + dy * step))

    def _respawn_rocks(self):
        if len(self.rocks) < ROCK_COUNT and random.random() < ROCK_RESPAWN_RATE:
            self.rocks.append(Rock(random.uniform(0, self.width), random.uniform(0, self.height)))

    def _point_in_water(self, x: float, y: float) -> bool:
        for zx, zy, zw, zh, _ in self.water_zones:
            if zx <= x <= zx + zw and zy <= y <= zy + zh:
                return True
        return False

    def _random_water_point(self) -> Tuple[float, float]:
        if not self.water_zones:
            return random.uniform(0, self.width), random.uniform(0, self.height)
        zx, zy, zw, zh, _ = random.choice(self.water_zones)
        return random.uniform(zx, zx + zw), random.uniform(zy, zy + zh)

    def _random_land_point(self) -> Tuple[float, float]:
        for _ in range(15):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            if not self._point_in_water(x, y):
                return x, y
        return random.uniform(0, self.width), random.uniform(0, self.height)

    def _nearest_water_point(self, x: float, y: float) -> Tuple[float, float]:
        if not self.water_zones:
            return None
        best = None
        best_dist = float('inf')
        for zx, zy, zw, zh, _ in self.water_zones:
            cx = zx + zw / 2
            cy = zy + zh / 2
            dist = (cx - x) ** 2 + (cy - y) ** 2
            if dist < best_dist:
                best = (cx, cy)
                best_dist = dist
        return best

    def _nearest_land_point(self, x: float, y: float) -> Tuple[float, float]:
        if not self.water_zones or not self._point_in_water(x, y):
            return (x, y)
        # Move horizontally toward nearest bank
        best = None
        best_dist = float('inf')
        for zx, zy, zw, zh, _ in self.water_zones:
            left_bank = zx
            right_bank = zx + zw
            for bank_x in (left_bank, right_bank):
                dist = abs(bank_x - x)
                if dist < best_dist:
                    best_dist = dist
                    best = (bank_x, y)
        return best if best else (x, y)

    def _remove_dead(self):
        """Remove dead entities and ensure non-negative counts."""
        for key in list(self.populations.keys()):
            self.populations[key] = [a for a in self.populations[key] if a.alive]
            # No logic to empty list if < 0 because it's impossible for len to be < 0

        self.food = [f for f in self.food if f.alive]
        self.rocks = [r for r in self.rocks if getattr(r, "alive", True)]
        self.shelters = [s for s in self.shelters if getattr(s, "alive", True)]

    def _maybe_trigger_event(self):
        """Random disasters to shake dynamics without wiping species."""
        for event_type, prob in EVENT_PROBABILITIES.items():
            if random.random() < prob:
                if event_type == "tsunami":
                    if not self.water_zones:
                        continue
                    center = self._random_water_point()
                    self._apply_event(event_type, center=center, radius=DISASTER_RADIUS)
                elif event_type == "earthquake":
                    center = self._random_land_point()
                    self._apply_event(event_type, center=center, radius=DISASTER_RADIUS)
                else:
                    center = (random.uniform(0, self.width), random.uniform(0, self.height))
                    self._apply_event(event_type, center=center, radius=DISASTER_RADIUS)

    def _apply_event(self, event_type: str, center: Tuple[float, float] = None, radius: float = None):
        severity = EVENT_SEVERITY.get(event_type, 1.0)
        max_casualties = {sp: max(1, int(len(agents) * MAX_EVENT_CASUALTY_FRACTION)) for sp, agents in self.populations.items()}
        casualties = {sp: 0 for sp in self.populations.keys()}
        shelters = self.shelters
        radius = radius or DISASTER_RADIUS

        for species, agents in self.populations.items():
            for agent in agents:
                if casualties[species] >= max_casualties[species]:
                    continue
                if center:
                    if agent.distance_to(center) > radius:
                        continue
                if event_type == "tsunami" and not self._point_in_water(*center):
                    continue
                if event_type == "earthquake" and self._point_in_water(*center):
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
        msg = f"Gen {self.generation} event: {event_type}{loc_text} (sev {severity:.1f})"
        self.extinction_log.append(msg)
        
        # UI Notification
        self.active_event_text = f"EVENT: {event_type.upper()}"
        self.active_event_timer = 180  # 3 seconds @ 60 FPS

    def build_shelter(self, rock: Rock, builder=None):
        """Convert rock into shelter."""
        if not getattr(rock, "alive", True):
            return
        rock.alive = False
        self.shelters.append(Shelter(rock.x, rock.y, radius=SHELTER_RADIUS))
        name = builder.species if builder else "agent"
        self.extinction_log.append(f"Gen {self.generation}: {name} built shelter")

    def apply_manual_event(self, event_type: str, position: Tuple[float, float], radius: float = DISASTER_RADIUS):
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
            if len(extinctions) == len(SPECIES_CLASS):
                self.run_history["extinctions"] += 1
                self.active_event_text = "MASS EXTINCTION!"
                self.active_event_timer = 300

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
            self.food.append(random_food(random.uniform(0, self.width), random.uniform(0, self.height)))
        # Respawn trees occasionally on new gen
        for _ in range(TREE_COUNT // 2): 
             self.food.append(PlantFood(random.uniform(0, self.width), random.uniform(0, self.height)))

        self.episode_step = 0
        self.generation += 1

    def _random_dna(self, species: str) -> DNA:
        ranges = SPECIES_DNA_RANGES[species]
        genes = {k: random.uniform(low, high) for k, (low, high) in ranges.items()}
        return DNA(genes, ranges)

    def reset_generation(self):
        """End episode early and restart."""
        self.run_history["manual_resets"] += 1
        self.end_episode()

    def reset_all(self, config_overrides=None):
        """Reset world and archive."""
        config_overrides = config_overrides or {}
        # Preserve history across resets if desired, or not?
        # User wants "how many times have this game started". I should probably preserve it if this is just "Reset All" button in the same session.
        history = self.run_history
        self.__init__(self.width, self.height, config_overrides)
        self.run_history["starts"] = history["starts"] + 1
        self.run_history["extinctions"] = history["extinctions"]
        self.run_history["manual_resets"] = history["manual_resets"]

    def get_all_agents(self):
        """Get all agents in the world."""
        result = []
        for agents in self.populations.values():
            result.extend(agents)
        return result
