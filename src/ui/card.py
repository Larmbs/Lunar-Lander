import pygame as pg

from .text import Display

"""
    Represents a collection of texts
    Can display multiple at a time with varying positions
    But it cannot change their look
"""


class Card(Display):
    def __init__(self, texts: list[Display]) -> None:
        self.texts = texts

    def render(self, surface: pg.Surface) -> None:
        for text in self.texts:
            text.render(surface)
