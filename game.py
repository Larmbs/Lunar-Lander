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
from src.entity.sprite.sprite import ImageSprite



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
        lander_image = pg.image.load(os.path.join(config.Assets.Folder, "lander.png"))
        sprite = ImageSprite(lander_image, 1, -90)
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
        padding = 80
        
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
        
        self.texts:list[ui.Display] = []
        
        # #Debugger
        # debug_display = ui.DebugDisplay()
        # debug_display.add_node(lambda:F"{self.config.Window.Title}", True)
        # debug_display.add_node(lambda:F"FPS {int(self.clock.get_fps())}", True)
        # self.texts.append(debug_display)
        
        #Fonts
        SystemFont = ui.Font("turretroadregular", 100, "white")
        SystemFontSmall = ui.Font("turretroadregular", 30, "white")
        Window = pg.Rect(0, 0, self.WIDTH, self.HEIGHT)
        Padding = 30
        WindowWithPadding = pg.Rect(Padding, Padding, self.WIDTH - Padding, self.HEIGHT - Padding)
        
        #Top Left Heads Up
        score = ui.Text("SCORE  0000", SystemFontSmall, (0,0), (500,50), "center_left")
        time = ui.Text( "TIME   0:00", SystemFontSmall, (0,0), (500,50), "center_left")
        fuel = ui.Text( "FUEL   0000", SystemFontSmall, (0,0), (500,50), "center_left")
        top_left_list = ui.MultiLineText([score, time, fuel], pg.Rect(0, 0, 300, 100))
        top_left = ui.Wrapper(top_left_list, WindowWithPadding, "top_left")
        top_left_heads_up = ui.Wrapper(top_left, Window, "center_center")
        self.texts.append(top_left_heads_up)
        
        #Top Right Heads Up
        altitude = ui.Text(        "ALTITUDE          0000", SystemFontSmall, (0,0), (500,50), "center_right")
        horizontal_speed = ui.Text("HORIZONTAL SPEED  0000", SystemFontSmall, (0,0), (500,50), "center_right")
        vertical_speed = ui.Text(  "VERTICAL SPEED    0000", SystemFontSmall, (0,0), (500,50), "center_right")
        top_right_list = ui.MultiLineText([altitude, horizontal_speed, vertical_speed], pg.Rect(0, 0, 400, 100))
        top_right = ui.Wrapper(top_right_list, WindowWithPadding, "top_right")
        top_right_heads_up = ui.Wrapper(top_right, Window, "center_center")
        self.texts.append(top_right_heads_up)
        
        #Low On Fuel Text
        text = ui.Text("LOW ON FUEL", SystemFontSmall, (0, 0), None, "center_center")
        wrap = ui.Wrapper(text, pg.Rect(0, 0, self.WIDTH, self.HEIGHT), "center_center")
        LOW_ON_FUEL = ui.FlashAble(wrap, 60, 60)
        self.texts.append(LOW_ON_FUEL)
        
        # self.event_checker.add_event(Event(pg.K_LEFT, lambda:self.texts.append(ui.MultiLineText([text1, text2, text3], pg.Rect(0, 0, self.WIDTH, self.HEIGHT)))))
        # self.event_checker.add_event(Event(pg.K_RIGHT, lambda:print(text2.rect, text2.pos)))

    
    
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
    