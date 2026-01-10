import random
from simulation.agents.agent import Agent
from simulation.config import CARCASS_ENERGY_VALUE


class Scavenger(Agent):
    """Prefers carcasses but will weakly hunt if hungry."""

    def __init__(self, x, y, world_width, world_height, dna, species="scavenger", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 120
        self.max_energy = 180

    def update(self, context):
        if not self.base_update():
            return

        carcasses = [f for f in context["food"] if getattr(f, "is_carcass", False)]
        regular_food = [f for f in context["food"] if not getattr(f, "is_carcass", False)]
        predators = context["populations"].get("hunter", [])
        grazer_targets = context["populations"].get("grazer", [])
        in_water = context["is_in_water"](self.x, self.y)
        nearest_land = context["nearest_land_point"](self.x, self.y) if in_water else None

        nearest_pred = self.find_nearest(predators)
        if nearest_pred and self.distance_to(nearest_pred) < self.vision * 0.8:
            self.move_away(nearest_pred.x, nearest_pred.y, speed_multiplier=1.2)
        else:
            # Prefer carcasses
            target_food = self.find_nearest(carcasses)
            if not target_food:
                target_food = self.find_nearest(regular_food)

            if target_food:
                self.move_towards(target_food.x, target_food.y, speed_multiplier=1.0)
                if self.distance_to(target_food) < self.size + 4 and target_food.alive:
                    target_food.alive = False
                    self.energy = min(self.max_energy, self.energy + (CARCASS_ENERGY_VALUE if getattr(target_food, "is_carcass", False) else 25))
                    self.metrics["energy_gained"] += CARCASS_ENERGY_VALUE
            else:
                # Light hunting if nothing else
                target = self.find_nearest(grazer_targets, max_distance=self.vision * 0.5)
                if target and random.random() < 0.35:
                    speed_mult = 0.7 if in_water else 1.05
                    self.move_towards(target.x, target.y, speed_multiplier=speed_mult)
                    if self.distance_to(target) < self.size + target.size:
                        target.alive = False
                        self.energy = min(self.max_energy, self.energy + 20)
                        self.metrics["kills"] += 1
                else:
                    if in_water and nearest_land:
                        self.move_towards(nearest_land[0], nearest_land[1], speed_multiplier=1.0)
                    else:
                        self.move()

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Scavenger") -> float:
        return agent.metrics["energy_gained"] * agent.dna.genes.get("carcass_affinity", 1.0) + agent.metrics["survival_time"] * 0.3
