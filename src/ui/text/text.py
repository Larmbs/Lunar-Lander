import pygame as pg

from .font import Font
from .consts import Displayable



class Text(Displayable):
    def __init__(self, text:str, font:Font, pos:tuple[int, int]) -> None:
        self.text = text
        self.font = font
        self.pos = pos
        
        self.to_display:bool = True
        
        self.surface:pg.Surface
        self.update_font()
        
    def change_pos(self, pos:tuple[int, int]) -> None:
        self.pos = pos
        
    def get_font(self) -> Font:
        return self.font
        
    def change_font(self, font:Font) -> None:
        self.font = font
        self.update_font()
        
    def change_text(self, text:str) -> None:
        self.text = text
        self.update_font()
        
    def display_on(self) -> None:
        self.to_display = True
        
    def display_off(self) -> None:
        self.to_display = False
        
    def update_font(self) -> None:
        self.surface = self.font.get_font().render(self.text, False, self.font.color, self.font.bg_color)
    
    def render(self, surface:pg.Surface) -> None:
        if self.to_display:
            surface.blit(self.surface, self.pos)
        