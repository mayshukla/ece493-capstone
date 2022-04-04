'''
Base class from which all game objects inherit.

Supports the implementation of the following requirements:
FR7 - Agent.HealthState
FR8 - Agent.RangedAttack
FR9 - Agent.Shields
FR10 - Agent.PositionState
FR11 - Agent.Movement
FR12 - Movement.Direction
FR13 - Movement.Speed
FR14 - Map.Walls
'''

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