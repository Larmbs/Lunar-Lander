import pygame as pg
from abc import ABC, abstractmethod



ColorValue = pg.Color | int | str | tuple[int, int, int]


class Displayable(ABC):
    @abstractmethod
    def render(self, surface:pg.Surface) -> None:
        ...
        