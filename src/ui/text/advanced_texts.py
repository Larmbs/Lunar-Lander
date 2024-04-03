from construct import OffsettedEnd
from numpy import rec
from yaml import AnchorToken
from .text import Text
import pygame as pg
from .display import Display


"""Helps to center text easier"""
class Wrapper(Display):
    def __init__(self, display:Display, rect:pg.Rect, anchor:str="left_top"):
        self.display = display
        self.rect = rect
        self.anchor = anchor
        
        self.offset = (0, 0)
        self.surface = pg.Surface((rect.width, rect.height), pg.SRCALPHA, 32)
        self.surface.convert_alpha()
        self.calc_offset()
        self.get_surface()
    
    def calc_offset(self):
        item_size = self.display.get_surface().get_rect()
        
        vert, hor = self.anchor.split("_")
        x_off, y_off = 0, 0
        
        # check for horizontal alignment specification
        if hor == "center": x_off = (self.rect.width - item_size.width)//2
        elif hor == "right": x_off = self.rect.width - item_size.width  
        # check for vertical alignment specification
        if vert == "center": y_off = (self.rect.height - item_size.height)//2
        elif vert == "bottom": y_off = self.rect.height - item_size.height
        
        self.offset = x_off, y_off       
        
    def render(self, surface:pg.Surface) -> None:       
        # pg.draw.rect(self.surface, "red", self.rect, 10)

        surface.blit(self.surface, (self.rect.left, self.rect.top))
    
    def get_surface(self) -> pg.Surface:
        self.surface.blit(self.display.get_surface(), self.offset)
        return self.surface
    
"""Allows to render multiline text easily"""
class MultiLineText(Display):
    def __init__(self, displays:list[Display], rect:pg.Rect|None=None, line_height:int|None=None) -> None:
        self.displays = displays
        self.rect = rect if rect else pg.Rect(0, 0, *self.calc_dim())
        self.line_height = line_height if line_height else self.calc_line_height()
        
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA, 32)
        self.surface.convert_alpha()
        
        self.update()
    
    def calc_dim(self) -> tuple[int, int]:
        widths = []
        sum_y = 0
        for display in self.displays:
            rect = display.get_surface().get_rect()
            sum_y += rect.height
            widths.append(rect.width)
        return max(widths), sum_y
        
    def calc_line_height(self) -> int:
        return self.rect.height // len(self.displays)
        
    def render(self, surface:pg.Surface) -> None:
        surface.blit(self.get_surface(), (self.rect.left, self.rect.top))
        
    def update(self) -> None:
        for index, display in enumerate(self.displays):
            display.rect = pg.Rect(self.rect.left, self.rect.top + index * self.line_height, self.rect.width, self.line_height)
            display.update()
            
    def get_surface(self) -> pg.Surface:
        for index, display in enumerate(self.displays):
            image = display.get_surface()
            self.surface.blit(image, (0, index*self.line_height))
        # pg.draw.rect(self.surface, "blue", self.rect, 10)
        return self.surface
        

"""Allows text to change display on or display off state""" 
class FlashAble(Display):
    EMPTY:pg.Surface = pg.Surface((0,0))
    
    def __init__(self, display:Display, on_time:int, off_time:int) -> None:
        self.display = display
        
        self.timer = 0
        self.loop_time = on_time + off_time
        self.on_time = on_time
        
    def get_surface(self) -> pg.Surface:
        self.timer += 1
        if self.timer % self.loop_time <= self.on_time:
            return self.display.get_surface()
        else:
            return self.EMPTY
        
    def render(self, surface:pg.Surface) -> None:
        self.timer += 1
        if self.timer % self.loop_time <= self.on_time:
            self.display.render(surface)
            