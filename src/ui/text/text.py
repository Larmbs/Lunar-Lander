import pygame as pg

from .font import Font
from .display import Display



class Text(Display):
    def __init__(self, text:str, font:Font, pos:tuple[int, int], dim:tuple[int, int]|None=None, anchor:str="top_left") -> None:
        self.text = text
        self.font = font
        self.pos = pos        
        
        self.anchor = anchor # describes position of text in the rect
        
        self.text_size = self.calc_text_dim()
        self.dim = dim if dim else self.text_size
        self.rect = pg.Rect(*pos, *self.dim)

        # surface is saved in object for easy loading and drawing
        self.offset = (0, 0)
        self.update()
    
    def calc_text_dim(self) -> tuple[int, int]:
        image = self.get_image().get_rect()
        return  image.width, image.height
        
    def get_image(self) -> pg.Surface:
        return self.font.get_font().render(self.text, True, self.font.color, self.font.bg_color)
        
    def calc_offset(self) -> None:
        hor, vert = self.anchor.split("_")
        x_off, y_off = 0, 0
        
        # check for horizontal alignment specification
        if hor == "center": x_off = (self.rect.width - self.text_size[0])//2
        elif hor == "right": x_off = self.rect.width - self.text_size[0]  
        # check for vertical alignment specification
        if vert == "center": y_off = (self.rect.height - self.text_size[1])//2
        elif vert == "bottom": y_off = self.rect.height - self.text_size[1]
        
        self.offset = x_off, y_off       
        
    def render(self, surface:pg.Surface) -> None:
        pos = self.pos[0]+self.offset[0],self.pos[1]+self.offset[1]
        surface.blit(self.surface, pos)
    
    def update(self) -> None:
        self.text_size = self.calc_text_dim()
        self.calc_offset()
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA, 32)
        self.surface.convert_alpha()
        self.surface.blit(self.get_image(), self.offset)
        
    def get_surface(self) -> pg.Surface:
        return self.surface
    