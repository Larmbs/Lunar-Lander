import pygame as pg

from .font import Font
from .display import Display



class Text(Display):
    def __init__(self, text:str, font:Font, pos:tuple[int, int], dim:tuple[int, int]|None=None, anchor:str="top_left") -> None:
        self.text = text
        self.font = font
        self.pos = pos
        
        self.offset:tuple[int, int] = (0, 0)
        
        self.anchor = anchor # describes position of text in the rect
        self.dim = dim

        # surface is saved in object for easy loading and drawing
        self.surface:pg.Surface
        # calc surface and any offsets
        self.update_font()
        self.update_rect()
        
    def update_rect(self) -> None:
        text_rect = self.surface.get_rect()
        self.rect = pg.Rect(text_rect.left, text_rect.top, text_rect.width, text_rect.height)
        
        if self.dim is not None:
            self.rect.width, self.rect.height = self.dim
        
        hor, vert = self.anchor.split("_")
        x_off, y_off = 0, 0
        
        # check for horizontal alignment specification
        if hor == "center": x_off = (self.rect.width - text_rect.width)//2
        elif hor == "right": x_off = self.rect.width - text_rect.width  
        # check for vertical alignment specification
        if vert == "center": y_off = (self.rect.height - text_rect.height)//2
        elif vert == "bottom": y_off = self.rect.height - text_rect.height
        
        self.offset = x_off, y_off       
        
    def update_font(self) -> None:
        self.surface = self.font.get_font().render(self.text, True, self.font.color, self.font.bg_color)
    
    def render(self, surface:pg.Surface) -> None:
        pos = self.pos[0]+self.offset[0],self.pos[1]+self.offset[1]
        surface.blit(self.surface, pos)
    
    def get_surface(self) -> tuple[pg.Surface, tuple[int, int]]:
        pos = self.pos[0]+self.offset[0],self.pos[1]+self.offset[1]
        return self.surface, pos