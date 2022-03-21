from src.object_state import ObjectState

class Obstacle(ObjectState):
    """Class containing properties that are common to moving objects."""

    def __init__(self, id, position, height, width):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the location of the center of the object.
            height: size paramter for obstacle
            width: size paramter for obstacle
        """
        super().__init__(id, position)
        self.height = height
        self.width = width