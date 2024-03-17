from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: float
    y: float
