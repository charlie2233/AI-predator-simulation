"""
Evolutionary utilities: selection, reproduction, archive handling.
"""
import random
from typing import Dict, List, Tuple
from simulation.evolution.dna import DNA
from simulation.config import MUTATION_SIGMA, TOURNAMENT_SIZE, ARCHIVE_TOP_K


class Archive:
    """Maintains top-K DNA samples per species."""

    def __init__(self, top_k: int = ARCHIVE_TOP_K):
        self.top_k = top_k
        self.store: Dict[str, List[Tuple[float, DNA]]] = {}

    def add_generation(self, species: str, scored: List[Tuple[float, DNA]]):
        """Record a generation's scored DNA."""
        if not scored:
            return
        bucket = self.store.setdefault(species, [])
        bucket.extend(scored)
        bucket.sort(key=lambda item: item[0], reverse=True)
        self.store[species] = bucket[: self.top_k]

    def sample(self, species: str, count: int, sigma_boost: float = 1.5) -> List[DNA]:
        """Sample DNA for recovery."""
        bucket = self.store.get(species, [])
        if not bucket:
            return []
        picks = []
        for _ in range(count):
            score, dna = random.choice(bucket)
            picks.append(dna.mutate(MUTATION_SIGMA * sigma_boost))
        return picks


def tournament_selection(scored: List[Tuple[float, DNA]], desired: int) -> List[DNA]:
    """Simple tournament selection."""
    selected: List[DNA] = []
    if not scored:
        return selected
    for _ in range(desired):
        contenders = random.sample(scored, min(TOURNAMENT_SIZE, len(scored)))
        best = max(contenders, key=lambda c: c[0])
        selected.append(best[1])
    return selected


def reproduce(selected: List[DNA], desired: int, sigma: float = MUTATION_SIGMA) -> List[DNA]:
    """Generate children via blend + mutation."""
    if not selected:
        return []
    children: List[DNA] = []
    for _ in range(desired):
        if len(selected) >= 2:
            a, b = random.sample(selected, 2)
        else:
            a = b = selected[0]
        alpha = random.uniform(0.35, 0.65)
        child = a.blend(b, alpha=alpha).mutate(sigma)
        children.append(child)
    return children
