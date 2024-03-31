from .colliders import Collider, CircleCollider, LineCollider, PolygonCollider

from .composite import TriangleCollider, QuadCollider, RectangleCollider, SquareCollider

from .collision_handler import CollisionHandler


"""
    Collider
    
    Colliders are bounds that define when an object is impacted or not
    A collider stores geometry dimensions to accurately detect when two
    different objects collide 
    
    There are two different categories of colliders
    Basic Colliders
    Advanced Colliders
    
    There are three types of Basic Colliders
        -Line Collider
        -Circle Collider
        -Polygon Collider
        
    These three colliders are the building blocks for all the rest
    
    
    Advanced Colliders expand on the basic colliders and may mix and match basic
    colliders behavior
    
    For Example:
        A Square Collider is a descendant from a polygon collider 
        A Triangle Collider is a descendant from a polygon collider

"""


BASIC_COLLIDERS = CircleCollider | LineCollider | PolygonCollider
ADVANCED_COLLIDERS = TriangleCollider | QuadCollider | RectangleCollider | SquareCollider

handle_collision = CollisionHandler().handle_collision



"""
    This is a module that provides collision detection and action according to it
    These are meant to help simulate basic collisions for arcade games
    
    Colliders have the collider body which is what is in physical space and the action that it 
    takes once a collision is felt
    There is a cool down on colliders to prevent over stimulation of action
    
    There are two types of colliders    
    Point/Circle Collider
    Line Colliders
    
    Using these two colliders you can construct many more complicated shapes
    This Module only allows for detection and will not be able to impart any action on 
    the physics object
    
    Colliders just hold basic data the physics object will pass in its current data to
    help the colliders better predict movement and so on
    
    A collider once it feels a collision will raise a has collided flag and then return 
    when collisions are checked a collision object that holds forces and basic acceleration 
    to be felt by the other object
"""
