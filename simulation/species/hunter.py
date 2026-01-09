import random
from simulation.agents.agent import Agent


class Hunter(Agent):
    """Predator that hunts grazers and scavengers."""

    def __init__(self, x, y, world_width, world_height, dna, species="hunter", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 140
        self.max_energy = 200

    def update(self, context):
        if not self.base_update():
            return

        prey_targets = context["populations"].get("grazer", []) + context["populations"].get("scavenger", [])
        protectors = context["populations"].get("protector", [])

        nearest_protector = self.find_nearest(protectors, max_distance=self.vision * 0.5)
        if nearest_protector and self.distance_to(nearest_protector) < nearest_protector.dna.genes.get("stun_radius", 30):
            self.move_away(nearest_protector.x, nearest_protector.y, speed_multiplier=1.1)
        else:
            target = self.find_nearest(prey_targets)
            if target:
                self.move_towards(target.x, target.y, speed_multiplier=1.25)
                attack_range = self.dna.genes.get("attack_range", 6) + self.size
                if self.distance_to(target) < attack_range and target.alive:
                    target.alive = False
                    self.energy = min(self.max_energy, self.energy + 45)
                    self.metrics["kills"] += 1
                    self.metrics["energy_gained"] += 45
            else:
                self.move()

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Hunter") -> float:
        return agent.metrics["kills"] * 50 + agent.metrics["survival_time"] * 0.2 + agent.metrics["energy_gained"]
