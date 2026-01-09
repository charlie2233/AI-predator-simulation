"""
Statistics collection and export helpers.
"""
import csv
import json
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class GenerationStats:
    generation: int
    counts: Dict[str, int]
    mean_dna: Dict[str, Dict[str, float]]
    extinction_events: List[str] = field(default_factory=list)


class StatsLogger:
    """Tracks per-generation stats."""

    def __init__(self):
        self.history: List[GenerationStats] = []

    def record(self, generation: int, counts: Dict[str, int], mean_dna: Dict[str, Dict[str, float]], extinctions: List[str]):
        self.history.append(GenerationStats(generation, counts, mean_dna, extinctions))

    def export_json(self, path: str):
        payload = [
            {
                "generation": item.generation,
                "counts": item.counts,
                "mean_dna": item.mean_dna,
                "extinction_events": item.extinction_events,
            }
            for item in self.history
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def export_csv(self, path: str):
        if not self.history:
            return
        # Flatten keys for quick glance
        species_keys = sorted({k for item in self.history for k in item.counts.keys()})
        fieldnames = ["generation"] + [f"{sp}_count" for sp in species_keys]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.history:
                row = {"generation": item.generation}
                row.update({f"{sp}_count": item.counts.get(sp, 0) for sp in species_keys})
                writer.writerow(row)
