import os
import pygame as pg
import numpy as np

from config import AppConfig
from src import (EventsChecker,
                 Event,Entity,
                 MoveableObject,
                 CircleSprite,
                 Lander,
                 TerrainSprite,
                 StaticObject,
                 Space)
from src.data import MapJSON, get_maps, PolygonJSON, get_polygons
from src import ui



POINT = list[float]

class Game:
    def __init__(self, config:AppConfig, clock:pg.time.Clock) -> None:
        self.config = config
        
        self.clock = clock
        
        self.WIDTH = config.Window.SizeX
        self.HEIGHT = config.Window.SizeY
        
        self.scroll:POINT = [0.0, 0.0]
        self.zoom = 0.2
        
        center_x = self.WIDTH//2
        center_y = self.HEIGHT//2


        self.space = Space((self.config.Game.AccelGravity, self.config.Game.AngleGravity), 2)
        
        self.surface = pg.Surface((self.WIDTH, self.HEIGHT))

        maps:list[MapJSON] = get_maps(os.path.join(config.Assets.Folder, config.Assets.Maps))
        polygons:list[PolygonJSON] = get_polygons(os.path.join(config.Assets.Folder, config.Assets.Polygons))
    
        """OBJECTS"""
        sprite = CircleSprite("blue", 50)
        phys = MoveableObject(5, 20, 20, 20, 0, 0, 0)
        self.lander = Lander(phys, sprite, 1500)
        self.space.add_object(self.lander)
        
        
        if isinstance(maps, list):
            mount = TerrainSprite("white", maps[0].Heights, maps[0].Vertical_Stretch, maps[0].Horizontal_Stretch, self.config.Game.TerrainThickness)
            static = StaticObject(0, 0, 0, 0)
            terrain = Entity(static, mount)
            self.space.add_object(terrain)
        
        """LISTENERS"""        
        self.event_checker = EventsChecker()
        self.event_checker.add_event(Event(pg.K_a, self.lander.turn_left))
        self.event_checker.add_event(Event(pg.K_d, self.lander.turn_right))
        self.event_checker.add_event(Event(pg.K_w, self.lander.thrust))
        
        #Screen Scroll Bounding Box
        padding = 50
        
        #X Scroll
        screen_range_x = range(-center_x + padding, center_x - padding)            
        def add_x_vel(): self.scroll[0] += phys.vx/100
        def is_in_bounds_x() -> bool: 
            screen_x = int((self.lander.active.x - self.scroll[0]) * self.zoom)
            return screen_x not in screen_range_x and np.sign(screen_x) == np.sign(phys.vx) # type: ignore
                
        #Y Scroll
        screen_range_y = range(-center_y + padding, center_y - padding)
        def add_y_vel() -> None: self.scroll[1] += phys.vy/100
        def is_in_bounds_y() -> bool:
            screen_y = int((self.lander.active.y - self.scroll[1]) * self.zoom)
            return screen_y not in screen_range_y and np.sign(screen_y) == np.sign(phys.vy) # type: ignore
        
        self.event_checker.add_event(Event(is_in_bounds_x, add_x_vel))
        self.event_checker.add_event(Event(is_in_bounds_y, add_y_vel))
        
        self.texts:list[ui.Displayable] = []
        
        # #Debugger
        # debug_display = ui.DebugDisplay()
        # debug_display.add_node(lambda:F"{self.config.Window.Title}", True)
        # debug_display.add_node(lambda:F"FPS {int(self.clock.get_fps())}", True)
        # self.texts.append(debug_display)
        
        #Test Text
        font = ui.Font("freesansbold.ttf", 100, "white")
        text = ui.Text("Hello World", font, (0,0), "right_bottom", pg.Rect(0, 0, self.WIDTH, self.HEIGHT))
        self.texts.append(text)
        
        self.event_checker.add_event(Event(pg.K_LEFT, text.display_off))
        self.event_checker.add_event(Event(pg.K_RIGHT, text.display_on))

    
    
    def update(self, dt:float) -> None:
        #Check For Inputs
        self.event_checker.handle_events()
        #Update Objects
        self.space.update(dt)
    
    def render(self) -> None:
        #Clear Screen
        self.surface.fill(pg.Color(0, 0, 0, 0))
        
        #Draw Objects
        for obj in self.space.objs:
            obj.draw(self.zoom, self.scroll, self.surface)
        
        #Draw Text
        for text in self.texts:
            if text.to_display:
                text.render(self.surface)
        
    def get_screen(self) -> pg.Surface:
        return self.surface
    