from dataclasses import dataclass

import pygame.font as pgf

from .displayable import ColorValue



@dataclass
class Font:
    family:str
    size:int
    
    color:ColorValue
    bg_color:ColorValue|None=None
    
    bold:bool=False
    underline:bool=False
    italic:bool=False
    strike:bool=False
    
    def get_font(self) -> pgf.Font:
        font = pgf.Font(self.family, self.size)
        font.set_bold(self.bold)
        font.set_underline(self.underline)
        font.set_italic(self.italic)
        font.set_strikethrough(self.strike)
        
        return font
    