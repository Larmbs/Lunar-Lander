from pydantic import BaseModel
import json


"""Sub Configs"""


class WindowConfig(BaseModel):
    Title: str
    DisplayFPS: bool
    SizeX: int
    SizeY: int


class AssetsConfig(BaseModel):
    Folder: str
    Icon: str
    Maps: str
    Polygons: str


class GameConfig(BaseModel):
    FrameRate: int
    TerrainThickness: int
    AccelGravity: int
    AngleGravity: float


"""Main Config"""


class AppConfig(BaseModel):
    Window: WindowConfig
    Assets: AssetsConfig
    Game: GameConfig


def get_config(file: str) -> AppConfig:
    with open(file, "r") as f:
        data = json.load(f)
    return AppConfig.model_validate(obj=data)
