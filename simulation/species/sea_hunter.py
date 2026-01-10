from simulation.agents.agent import Agent


class SeaHunter(Agent):
    """Hunter specialized for water zones; slower on land."""

    def __init__(self, x, y, world_width, world_height, dna, species="sea_hunter", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 160
        self.max_energy = 220

    def update(self, context):
        if not self.base_update():
            return

        in_water = context["is_in_water"](self.x, self.y)
        nearest_water = context["nearest_water_point"](self.x, self.y)
        nearest_land = context["nearest_land_point"](self.x, self.y) if in_water else None
        prey_targets = context["populations"].get("grazer", []) + context["populations"].get("scavenger", [])

        # Prefer to stay near water
        if not in_water and nearest_water:
            self.move_towards(nearest_water[0], nearest_water[1], speed_multiplier=1.1)
        else:
            target = self.find_nearest(prey_targets)
            if target:
                swim_factor = self.dna.genes.get("swim_factor", 1.0)
                speed_mult = 1.0 + 0.3 * swim_factor if in_water else 0.6
                self.move_towards(target.x, target.y, speed_multiplier=speed_mult)
                if self.distance_to(target) < (self.size + target.size):
                    dmg = self.dna.genes.get("attack_power", 32)
                    target.take_damage(dmg)
                    self.energy = min(self.max_energy, self.energy + 30)
                    self.metrics["kills"] += 1 if not target.alive else 0
                    self.metrics["damage_done"] += dmg
            else:
                if in_water:
                    self.move()
                elif nearest_water:
                    self.move_towards(nearest_water[0], nearest_water[1], speed_multiplier=1.0)
                elif nearest_land:
                    self.move_towards(nearest_land[0], nearest_land[1], speed_multiplier=0.8)

        self.clamp_position()

    @staticmethod
    def fitness(agent: "SeaHunter") -> float:
        return agent.metrics["kills"] * 50 + agent.metrics["survival_time"] * 0.4
