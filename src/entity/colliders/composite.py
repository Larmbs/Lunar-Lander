from .colliders import PolygonCollider
import numpy as np


class TriangleCollider(PolygonCollider):
    def __init__(self, vertex1: np.ndarray, vertex2: np.ndarray, vertex3: np.ndarray, offset: np.ndarray) -> None:
        super().__init__([vertex1, vertex2, vertex3, vertex1], offset)


class QuadCollider(PolygonCollider):
    def __init__(self, vertex1: np.ndarray, vertex2: np.ndarray, vertex3: np.ndarray, vertex4: np.ndarray, offset: np.ndarray) -> None:
        super().__init__([vertex1, vertex2, vertex3, vertex4, vertex1], offset)


class RectangleCollider(QuadCollider):
    def __init__(self, width: int, height: int, rotation: float, offset: np.ndarray) -> None:
        # Calculating vertices
        half_width = width / 2
        half_height = height / 2
        # Vertices of the unrotated rectangle
        vertices = np.array([[-half_width, half_height],
                             [half_width, half_height],
                             [half_width, -half_height],
                             [-half_width, -half_height]])
        # Rotation matrix
        rotation_matrix = np.array([[np.cos(rotation), -np.sin(rotation)],
                                    [np.sin(rotation), np.cos(rotation)]])
        # Rotate vertices
        rotated_vertices = np.dot(vertices, rotation_matrix)
        # Apply offset
        v1, v2, v3, v4 = rotated_vertices
        super().__init__(v1, v2, v3, v4, offset)


class SquareCollider(RectangleCollider):
    def __init__(self, side_len: int, rotation: float, offset: np.ndarray) -> None:
        super().__init__(side_len, side_len, rotation, offset)
