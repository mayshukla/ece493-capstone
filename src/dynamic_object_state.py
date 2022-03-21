from src.object_state import ObjectState

class DynamicObjectState(ObjectState):
    """Class containing properties that are common to moving objects."""

    def __init__(self, id, position, velocity):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the location of the center of the object.
            velocity: a vector2 object representing the object's initial velocity.
        """
        super().__init__(id, position)
        self.velocity = velocity