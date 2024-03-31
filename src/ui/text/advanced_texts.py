from .text import Text
from .font import Font
import pygame as pg



class FlashAble(Text):
    def __init__(self, text:str, font:Font, pos:tuple[int, int], on_time:int, off_time:int) -> None:
        super().__init__(text, font, pos)
        self.timer = 0
        self.loop_time = on_time + off_time
        self.on_time = on_time
        
    def render(self, surface:pg.Surface) -> None:
        if self.to_display:
            self.timer += 1
            if self.timer % self.loop_time <= self.on_time:
                surface.blit(self.surface, self.pos)
            