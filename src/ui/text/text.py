import pygame as pg

from .font import Font
from .displayable import Displayable



class Text(Displayable):
    def __init__(self, text:str, font:Font, pos:tuple[int, int], anchor:str="top_left", rect:pg.Rect|None=None) -> None:
        self.text = text
        self.font = font
        self.pos = pos
        
        self.anchor = anchor # describes position of text in the rect
        
        self.rect:pg.Rect|None = rect # rect which is meant to contain the text as best as it can

        # surface is saved in object for easy loading and drawing
        self.surface:pg.Surface
        # calc surface and any offsets
        self.update_font()
        self.update_rect()
        
    def change_font(self, font:Font) -> None:
        self.font = font
        self.update_font()
        
    def change_text(self, text:str) -> None:
        self.text = text
        self.update_font()
        
    def update_rect(self) -> None:
        text_rect = self.surface.get_rect()
        if not self.rect: self.rect = text_rect # if no rect is specified just use the default size 
        else: # else apply anchor to custom rect to position text as wanted
            hor, vert = self.anchor.split("_")
            x_off, y_off = 0, 0
            
            # check for horizontal alignment specification
            if hor == "center": x_off = (self.rect.width - text_rect.width)//2
            elif hor == "right": x_off = self.rect.width - text_rect.width  
            # check for vertical alignment specification
            if vert == "center": y_off = (self.rect.height - text_rect.height)//2
            elif vert == "bottom": y_off = self.rect.height - text_rect.height
            
            #offsetting default pos by needed amount
            self.pos = self.pos[0]+x_off, self.pos[1]+y_off
        
    def update_font(self) -> None:
        self.surface = self.font.get_font().render(self.text, True, self.font.color, self.font.bg_color)
    
    def render(self, surface:pg.Surface) -> None:
        surface.blit(self.surface, self.pos)
        