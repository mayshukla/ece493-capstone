from vector2 import Vector2
from object_state import ObjectState

class DynamicObjectState(ObjectState):
    """Class containing properties that are common to moving objects."""

    def __init__(self, id, position, velocity):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the object's initial position.
            velocity: a vector2 object representing the object's initial velocity.
        """
        super().__init__(id, position)
        self.velocity = velocity