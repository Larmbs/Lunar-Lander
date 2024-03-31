from .text import Text
import pygame as pg
from .displayable import Displayable
from typing import Callable


class MultiLineText(Displayable):
    pass


COLOR_FUNC = Callable[[int], tuple[int, int, int]]
class ColorChanging(Displayable):
    def __init__(self, text:Text, func:COLOR_FUNC) -> None:
        pass
    
    
class FlashAble(Displayable):
    def __init__(self, text:Text, on_time:int, off_time:int) -> None:
        self.text = text
        self.timer = 0
        self.loop_time = on_time + off_time
        self.on_time = on_time
        
    def render(self, surface:pg.Surface) -> None:
        self.timer += 1
        if self.timer % self.loop_time <= self.on_time:
            self.text.render(surface)
            