import random
from simulation.agents.agent import Agent


class Protector(Agent):
    """Escorts grazers and can stun hunters at close range."""

    def __init__(self, x, y, world_width, world_height, dna, species="protector", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 130
        self.max_energy = 190

    def update(self, context):
        if not self.base_update():
            return

        grazers = context["populations"].get("grazer", [])
        predators = context["populations"].get("hunter", [])
        rocks = context.get("rocks", [])
        build_shelter = context.get("build_shelter")

        # Escort nearest grazer
        escort = self.find_nearest(grazers, max_distance=self.vision)
        if escort:
            self.move_towards(escort.x, escort.y, speed_multiplier=0.9)
        else:
            self.move()

        # Convert rock to shelter if nearby
        rock = self.find_nearest(rocks, max_distance=self.size + 10)
        if rock and getattr(rock, "alive", True) and build_shelter and self.energy > 40:
            build_shelter(rock, builder=self)
            self.energy -= 5

        stun_radius = self.dna.genes.get("stun_radius", 30)
        stun_cd = int(self.dna.genes.get("stun_cooldown", 120))
        for pred in predators:
            if pred.alive and self.distance_to(pred) < stun_radius and self.cooldowns.get("stun_ready", 0) == 0:
                pred.cooldowns["stunned"] = 30
                pred.cooldowns["slowed"] = 60
                self.cooldowns["stun_ready"] = stun_cd
                self.metrics["stuns"] += 1
                break

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Protector") -> float:
        return agent.metrics["stuns"] * 40 + agent.metrics["survival_time"] * 0.4
