from abc import ABC
import numpy as np


class Collider(ABC):
    def __init__(self, offset: np.ndarray) -> None:
        self.offset = offset

    def get_center(self, pos: np.ndarray) -> np.ndarray:
        return pos + self.offset


class LineCollider(Collider):
    def __init__(self, point1: np.ndarray, point2: np.ndarray, offset: np.ndarray) -> None:
        super().__init__(offset)
        self.point1 = point1
        self.point2 = point2


class CircleCollider(Collider):
    def __init__(self, radius: float, offset: np.ndarray) -> None:
        super().__init__(offset)
        self.radius = radius


class PolygonCollider(Collider):
    def __init__(self, vertices: list[np.ndarray], offset: np.ndarray) -> None:
        super().__init__(offset)
        self.vertices = vertices
