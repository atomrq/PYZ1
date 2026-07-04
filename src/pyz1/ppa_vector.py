from __future__ import annotations

from dataclasses import dataclass

from pyz1.models import Vector3


@dataclass(frozen=True, slots=True)
class PpaVector:
    x: float
    y: float
    z: float


def add_vectors(first: PpaVector, second: PpaVector) -> PpaVector:
    return PpaVector(first.x + second.x, first.y + second.y, first.z + second.z)


def subtract_vectors(first: PpaVector, second: PpaVector) -> PpaVector:
    return PpaVector(first.x - second.x, first.y - second.y, first.z - second.z)


def scale_vector(vector: PpaVector, scale: float) -> PpaVector:
    return PpaVector(vector.x * scale, vector.y * scale, vector.z * scale)


def dot_vectors(first: PpaVector, second: PpaVector) -> float:
    return first.x * second.x + first.y * second.y + first.z * second.z


def zero_vector() -> PpaVector:
    return PpaVector(0.0, 0.0, 0.0)


def vector_from_model(vector: Vector3) -> PpaVector:
    return PpaVector(vector.x, vector.y, vector.z)


def vector_to_model(vector: PpaVector) -> Vector3:
    return Vector3(vector.x, vector.y, vector.z)
