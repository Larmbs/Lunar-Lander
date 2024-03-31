import pygame as pg

from .text import Displayable

"""
    Represents a collection of texts
    Can display multiple at a time with varying positions
    But it cannot change their look
"""

class Card(Displayable):
    def __init__(self, texts:list[Displayable]) -> None:
        self.texts = texts
        
    def render(self, surface:pg.Surface) -> None:
        for text in self.texts:
            text.render(surface)
            