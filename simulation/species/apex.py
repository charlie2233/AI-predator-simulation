from simulation.agents.agent import Agent


class Apex(Agent):
    """Tertiary hunter that targets most other land agents."""

    def __init__(self, x, y, world_width, world_height, dna, species="apex", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 180
        self.max_energy = 240

    def update(self, context):
        if not self.base_update():
            return

        prey_targets = []
        for name in ("hunter", "grazer", "scavenger", "protector"):
            prey_targets.extend(context["populations"].get(name, []))
        in_water = context["is_in_water"](self.x, self.y)
        nearest_land = context["nearest_land_point"](self.x, self.y) if in_water else None

        # Avoid shelters? Apex is bold, ignores unless stunned
        target = self.find_nearest(prey_targets)
        if target:
            speed_mult = 0.6 if in_water else 1.3
            self.move_towards(target.x, target.y, speed_multiplier=speed_mult)
            if self.distance_to(target) < (self.size + target.size + self.dna.genes.get("attack_range", 8)):
                target.alive = False
                self.energy = min(self.max_energy, self.energy + 55)
                self.metrics["kills"] += 1
        else:
            if in_water and nearest_land:
                self.move_towards(nearest_land[0], nearest_land[1], speed_multiplier=1.0)
            else:
                self.move()

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Apex") -> float:
        return agent.metrics["kills"] * 70 + agent.metrics["survival_time"] * 0.3
