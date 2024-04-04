from .physics import PhysicsBody
from .sprite import Sprite
from .colliders import Collider
import pygame as pg


class Entity:
    def __init__(self, physics: PhysicsBody, sprite: Sprite, collider: Collider | None = None) -> None:
        self.active = physics
        self.sprite = sprite
        self.collider = collider

    def get_physics(self) -> PhysicsBody:
        return self.active

    def get_sprite(self) -> Sprite:
        return self.sprite

    def get_collider(self) -> Collider | None:
        return self.collider

    def draw(self, zoom: float, scroll: list[float], surface: pg.Surface) -> None:
        self.sprite.draw(self.active.get_pos(), self.active.rot,
                         zoom, (int(scroll[0]), int(scroll[1])), surface)
