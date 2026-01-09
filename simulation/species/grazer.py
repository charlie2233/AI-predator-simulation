import random
from simulation.agents.agent import Agent
from simulation.config import FOOD_ENERGY_VALUE


class Grazer(Agent):
    """Plant-eating prey that prefers staying with the herd."""

    def __init__(self, x, y, world_width, world_height, dna, species="grazer", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 110
        self.max_energy = 170

    def update(self, context):
        if not self.base_update():
            return

        food_items = context["food"]
        predators = context["populations"].get("hunter", []) + context["populations"].get("parasite", [])
        protectors = context["populations"].get("protector", [])
        grazers = context["populations"].get("grazer", [])
        rocks = context.get("rocks", [])
        shelters = context.get("shelters", [])
        build_shelter = context.get("build_shelter")

        nearest_predator = self.find_nearest(predators)
        if nearest_predator and self.distance_to(nearest_predator) < self.vision:
            self.move_away(nearest_predator.x, nearest_predator.y, speed_multiplier=1.4)
        else:
            # Cohesion/dispersion balance
            cohesion = self.dna.genes.get("cohesion", 0.4)
            dispersion = self.dna.genes.get("dispersion", 0.3)
            neighbors = [g for g in grazers if g is not self and g.alive and self.distance_to(g) < self.vision * 0.6]
            if neighbors:
                avg_x = sum(g.x for g in neighbors) / len(neighbors)
                avg_y = sum(g.y for g in neighbors) / len(neighbors)
                if cohesion > dispersion:
                    self.move_towards(avg_x, avg_y, speed_multiplier=0.9)
                else:
                    self.move_away(avg_x, avg_y, speed_multiplier=0.8)

            target_food = self.find_nearest(food_items)
            if target_food:
                self.move_towards(target_food.x, target_food.y, speed_multiplier=1.0)
                if self.distance_to(target_food) < self.size + 4 and target_food.alive:
                    target_food.alive = False
                    self.energy = min(self.max_energy, self.energy + FOOD_ENERGY_VALUE)
                    self.metrics["energy_gained"] += FOOD_ENERGY_VALUE
            else:
                self.move()

        # Stay close to protectors if nearby
        protector = self.find_nearest(protectors, max_distance=self.vision * 0.5)
        if protector:
            self.move_towards(protector.x, protector.y, speed_multiplier=0.8)

        # Build shelter if a rock is handy
        rock = self.find_nearest(rocks, max_distance=self.size + 8)
        if rock and getattr(rock, "alive", True) and build_shelter and random.random() < 0.1:
            build_shelter(rock, builder=self)

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Grazer") -> float:
        return agent.metrics["survival_time"] * 0.6 + agent.metrics["energy_gained"] * 0.4
