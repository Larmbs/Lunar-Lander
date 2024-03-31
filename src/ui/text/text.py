import pygame as pg

from .font import Font
from .displayable import Displayable



class Text(Displayable):
    def __init__(self, text:str, font:Font, pos:tuple[int, int], anchor:str="top_left", rect:pg.Rect|None=None) -> None:
        self.text = text
        self.font = font
        self.pos = pos
        
        self.anchor = anchor
        self.surface:pg.Surface
        self.rect:pg.Rect|None = rect
        
        self.to_display:bool = True
        
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
        
    def update_font(self) -> None:
        self.surface = self.font.get_font().render(self.text, False, self.font.color, self.font.bg_color)
        if not self.rect:
            self.rect = self.surface.get_rect()
        else:
            text_rect = self.surface.get_rect()
            horz, vert = self.anchor.split("_")
            x_off = 0
            y_off = 0
            
            if horz == "center":
                x_off = (self.rect.width - text_rect.width)//2
            elif horz == "right":
                x_off = self.rect.width - text_rect.width
                
            if vert == "center":
                y_off = (self.rect.height - text_rect.height)//2
            elif vert == "bottom":
                y_off = self.rect.height - text_rect.height
                
            self.pos = self.pos[0]+x_off, self.pos[1]+y_off
 
    
    def render(self, surface:pg.Surface) -> None:
        surface.blit(self.surface, self.pos, self.rect)
        