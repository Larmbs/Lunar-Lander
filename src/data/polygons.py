from pydantic import BaseModel, ValidationError
import json


POINT = tuple[float, float]
ColorValue = tuple[int, int, int]

class PolygonJSON(BaseModel):
    Points:list[POINT]
    Color:ColorValue
    
def get_polygons(json_file:str) -> list[PolygonJSON]:
    with open(json_file, "r") as f:
        data = json.load(fp=f)
        
    result:list[PolygonJSON] = []
    if not isinstance(data, list):
        data = [data]
        
    for model in data:
        try:
            result.append(PolygonJSON.model_validate(model))
        except ValidationError as e:
            raise e
    
    return result
