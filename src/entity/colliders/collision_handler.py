from .colliders import CircleCollider, PolygonCollider, Collider, LineCollider
import numpy as np
from pygame import math



def line_line_collider(l1_p1:np.ndarray, l1_p2:np.ndarray, l2_p1:np.ndarray, l2_p2:np.ndarray) -> bool:
    P  = math.Vector2(*l1_p1)
    line1_vec = math.Vector2(*l1_p2) - P
    R = line1_vec.normalize()
    Q  = math.Vector2(*l2_p1)
    line2_vec = math.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()

    RNV = math.Vector2(R[1], -R[0])
    SNV = math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False
    
    QP  = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN
    
    return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

def line_line_collision(l1:LineCollider, pos1:np.ndarray, l2:LineCollider, pos2:np.ndarray) -> bool:
    l1_p1 = l1.point1 + pos1
    l1_p2 = l1.point2 + pos1
    l2_p1 = l2.point1 + pos2
    l2_p2 = l2.point2 + pos2
    return line_line_collider(l1_p1, l1_p2, l2_p1, l2_p2)

def circle_circle_collision(circle1:CircleCollider, pos1:np.ndarray, circle2:CircleCollider, pos2:np.ndarray) -> bool:
    x1, y1 = circle1.get_center(pos1)
    x2, y2 = circle2.get_center(pos2)
    return (x1 - x2)**2 + (y1 - y2)**2 <= circle1.radius + circle2.radius

def polygon_polygon_collision(polygon1:PolygonCollider, pos1: np.ndarray, polygon2:PolygonCollider, pos2: np.ndarray) -> bool:
    world_vertices1 = [vertex + pos1 for vertex in polygon1.vertices]
    world_vertices2 = [vertex + pos2 for vertex in polygon2.vertices]
    
    for i in range(len(world_vertices1)-1):
        for j in range(len(world_vertices2)-1):
            if line_line_collider(world_vertices1[i], world_vertices1[i+1], world_vertices2[j], world_vertices2[j+1]):
                return True
    return False

def polygon_line_collision(line:LineCollider, pos1: np.ndarray, polygon:PolygonCollider, pos2: np.ndarray) -> bool:
    x1, y1 = line.point1 + pos1
    x2, y2 = line.point2 + pos1
    
    vertices = [vertex + pos2 for vertex in polygon.vertices]
    
    for i in range(len(vertices)-1):
        if line_line_collider(np.array([x1, y1]), np.array([x2, y2]), vertices[i], vertices[i+1]):
            return True
    return False

class CollisionHandler:
    def handle_collision(self, collider1:Collider, pos1: np.ndarray, collider2:Collider, pos2: np.ndarray) -> bool:
        
        if isinstance(collider1, CircleCollider) and isinstance(collider2, CircleCollider):
            return circle_circle_collision(collider1, pos1, collider2, pos2)
        elif isinstance(collider1, LineCollider) and isinstance(collider2, LineCollider):
            return line_line_collision(collider1, pos1, collider2, pos2)
        elif isinstance(collider1, PolygonCollider) and isinstance(collider2, PolygonCollider):
            return polygon_polygon_collision(collider1, pos1, collider2, pos2)
        elif isinstance(collider1, PolygonCollider) and isinstance(collider2, LineCollider):
            return polygon_line_collision(collider2, pos2, collider1, pos1)
        elif isinstance(collider1, LineCollider) and isinstance(collider2, PolygonCollider):
            return polygon_line_collision(collider1, pos1, collider2, pos2)
        else:
            return False
    