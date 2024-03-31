import pygame as pg
from abc import ABC, abstractmethod



ColorValue = pg.Color | int | str | tuple[int, int, int]

class Displayable(ABC):
    to_display:bool
    
    @abstractmethod
    def render(self, surface:pg.Surface) -> None:
        ...
        
    def display_on(self) -> None:
        self.to_display = True
    def display_off(self) -> None:
        self.to_display = False
        