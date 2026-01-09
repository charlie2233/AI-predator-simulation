"""
DNA utilities for evolutionary steps.
"""
import copy
import random
from typing import Dict, Tuple


class DNA:
    """Dict-like DNA container with mutation helpers."""

    def __init__(self, genes: Dict[str, float], ranges: Dict[str, Tuple[float, float]]):
        self.genes = dict(genes)
        self.ranges = ranges

    def copy(self) -> "DNA":
        """Return a deep copy of the DNA."""
        return DNA(copy.deepcopy(self.genes), self.ranges)

    def mutate(self, sigma: float) -> "DNA":
        """Gaussian mutate each gene, clamped to configured ranges."""
        mutated = self.copy()
        for key, value in mutated.genes.items():
            low, high = mutated.ranges.get(key, (value * 0.5, value * 1.5))
            noise = random.gauss(0, sigma * max(1e-3, (high - low)))
            mutated.genes[key] = _clamp(value + noise, low, high)
        return mutated

    def blend(self, other: "DNA", alpha: float = 0.5) -> "DNA":
        """Blend two DNAs together."""
        blended = {}
        for key in self.genes.keys():
            a = self.genes[key]
            b = other.genes.get(key, a)
            blended[key] = a * alpha + b * (1 - alpha)
        return DNA(blended, self.ranges)

    def to_dict(self) -> Dict[str, float]:
        return dict(self.genes)


def _clamp(val: float, low: float, high: float) -> float:
    return max(low, min(high, val))
