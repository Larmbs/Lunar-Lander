from .entity import Entity


class Space:
    def __init__(self, gravity:tuple[int, float], physics_steps:int) -> None:
        self.physics_steps = physics_steps
        self.objs:list[Entity] = []
        
        self.gravity = gravity
        
    def add_object(self, entity:Entity) -> None:
        self.objs.append(entity)
        
    def update(self, dt:float) -> None:
        for obj in self.objs:
            obj.active.apply_accel(*self.gravity, dt)
            obj.active.update(dt)
            
        self.resolve_collisions(dt)
              
    def resolve_collisions(self, dt:float) -> None:
        t = dt/self.physics_steps
        for _ in range(self.physics_steps):
            ...
            