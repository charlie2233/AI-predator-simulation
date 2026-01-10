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
        in_water = context["is_in_water"](self.x, self.y)
        nearest_land = context["nearest_land_point"](self.x, self.y) if in_water else None

        # Escort nearest grazer
        escort = self.find_nearest(grazers, max_distance=self.vision)
        if escort:
            speed_mult = 0.7 if in_water else 0.9
            self.move_towards(escort.x, escort.y, speed_multiplier=speed_mult)
        else:
            if in_water and nearest_land:
                self.move_towards(nearest_land[0], nearest_land[1], speed_multiplier=1.0)
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
                pred.take_damage(15)
                self.metrics["damage_done"] += 15
                self.cooldowns["stun_ready"] = stun_cd
                self.metrics["stuns"] += 1
                break

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Protector") -> float:
        return agent.metrics["stuns"] * 40 + agent.metrics["survival_time"] * 0.4
