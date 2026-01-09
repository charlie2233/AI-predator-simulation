import random
from simulation.agents.agent import Agent


class Parasite(Agent):
    """Attaches to hosts to drain energy and slow them."""

    def __init__(self, x, y, world_width, world_height, dna, species="parasite", clan=None):
        super().__init__(x, y, world_width, world_height, dna, species, clan=clan)
        self.energy = 90
        self.max_energy = 140
        self.attached_to = None
        self.attach_timer = 0

    def update(self, context):
        if not self.base_update():
            return

        hosts = []
        for name in ("grazer", "hunter", "scavenger", "protector"):
            hosts.extend(context["populations"].get(name, []))

        drain_rate = self.dna.genes.get("drain_rate", 0.8)
        attach_time = int(self.dna.genes.get("attach_time", 120))

        if self.attached_to and getattr(self.attached_to, "alive", False):
            self.x, self.y = self.attached_to.x, self.attached_to.y
            self.attach_timer += 1
            self.energy = min(self.max_energy, self.energy + drain_rate)
            self.metrics["attachments"] += drain_rate
            self.attached_to.energy -= drain_rate * 0.6
            self.attached_to.cooldowns["slowed"] = 20
            if self.attach_timer >= attach_time or self.attached_to.energy <= 0:
                self.attached_to = None
                self.attach_timer = 0
        else:
            target = self.find_nearest(hosts)
            if target and self.distance_to(target) < self.size + 4:
                if self.cooldowns.get("attach_cd", 0) == 0:
                    self.attached_to = target
                    self.attach_timer = 0
                    self.cooldowns["attach_cd"] = 100
            else:
                self.move_towards(target.x, target.y, speed_multiplier=1.2) if target else self.move()

        self.clamp_position()

    @staticmethod
    def fitness(agent: "Parasite") -> float:
        return agent.metrics["attachments"] * 30 + agent.metrics["survival_time"] * 0.3
