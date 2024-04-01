from numpy import rec
from .text import Text
import pygame as pg
from .display import Display


"""Helps to center text easier"""
class Wrapper(Display):
    def __init__(self):
        pass
    
"""Allows to render multiline text easily"""
class MultiLineText(Display):
    def __init__(self, texts:list[Text], rect:pg.Rect, line_height:int|None=None) -> None:
        self.texts = texts
        self.rect = rect
        self.line_height = line_height
        self.calculate_rects()
        
    def calculate_rects(self) -> None:
        if self.line_height is None:
            text_height = self.rect.height // len(self.texts)
        else:
            text_height = self.line_height
        
        for index, text in enumerate(self.texts):
            text.pos = self.rect.left, self.rect.top + index * text_height
            text.dim = self.rect.width, text_height
         
            text.update_rect() 
        
    def render(self, surface:pg.Surface) -> None:
        # pg.draw.rect(surface, [0, 200, 255], self.rect, 20)
        for text in self.texts:
            image, pos = text.get_surface()
            surface.blit(image, pos)

"""Allows text to change display on or display off state""" 
# class FlashAble(Text):
#     def __init__(self, text:Text, on_time:int, off_time:int) -> None:
#         super().__init__(text.text, text.font, text.pos, text.dim, text.anchor)
#         self.timer = 0
#         self.loop_time = on_time + off_time
#         self.on_time = on_time
        
#     def render(self, surface:pg.Surface) -> None:
#         self.timer += 1
#         if self.timer % self.loop_time <= self.on_time:
#             super().render(surface)
            