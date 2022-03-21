class ObjectState():
    """Base class containing properties that are common to all types of objects."""

    def __init__(self, id, position):
        """Constructor

        Arguments:
            id: unique int id
            position: position: a vector2 object representing the location of the center of the object.
        """
        self.id = id
        self.position = position