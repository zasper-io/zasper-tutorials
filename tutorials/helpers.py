"""Small helpers used by 08-code-intelligence.ipynb."""

import csv
from collections import Counter
from dataclasses import dataclass
from statistics import mean


@dataclass
class Penguin:
    species: str
    island: str
    bill_length_mm: float
    bill_depth_mm: float
    flipper_mm: float
    mass_g: float
    sex: str
    year: int


def load_penguins(path: str) -> list[Penguin]:
    """Read the Palmer Penguins CSV, skipping rows with missing values."""
    with open(path, newline="") as file:
        rows = [row for row in csv.DictReader(file) if "NA" not in row.values()]
    return [
        Penguin(
            species=row["species"],
            island=row["island"],
            bill_length_mm=float(row["bill_length_mm"]),
            bill_depth_mm=float(row["bill_depth_mm"]),
            flipper_mm=float(row["flipper_length_mm"]),
            mass_g=float(row["body_mass_g"]),
            sex=row["sex"],
            year=int(row["year"]),
        )
        for row in rows
    ]


def describe_penguins(penguins: list[Penguin]) -> dict[str, dict[str, float]]:
    """Count the penguins of each species and average their body mass in grams."""
    counts = Counter(p.species for p in penguins)
    return {
        species: {
            "count": count,
            "mean_mass_g": round(mean(p.mass_g for p in penguins if p.species == species), 1),
        }
        for species, count in sorted(counts.items())
    }
