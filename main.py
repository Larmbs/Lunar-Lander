import os
import sys

import pygame as pg

from config import get_config, AppConfig
from game import Game


class App:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.RES = config.Window.SizeX, config.Window.SizeY

        # Initializing Pygame Modules
        pg.init()
        pg.font.init()

        # Getting Game Objects
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        # Customizing Window
        pg.display.set_caption(config.Window.Title)
        icon = pg.image.load(
            os.path.join(config.Assets.Folder, config.Assets.Icon)
        )
        pg.display.set_icon(icon)

        # Creating Game Instance
        self.game = Game(config, self.clock)

    def run(self) -> None:
        while True:
            # Getting Delta Time
            dt = self.clock.tick(self.config.Game.FrameRate) / 1000

            # Updating Game State
            self.game.update(dt)

            # Checking For Exit Event
            [self.exit() for event in pg.event.get() if event.type == pg.QUIT]

            # Rendering Game
            self.game.render()
            self.screen.blit(self.game.get_screen(), (0, 0))

            # Updating Display
            pg.display.flip()

    def exit(self) -> None:
        pg.quit()
        sys.exit()


def main() -> None:
    CONFIG = get_config("config.json")
    app = App(CONFIG)
    app.run()


if __name__ == "__main__":
    main()
