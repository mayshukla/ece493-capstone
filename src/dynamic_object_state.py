'''
Base class from which all moving objects in the game inherit.

Part of the implementation of the following requirements:
FR7 - Agent.HealthState
FR8 - Agent.RangedAttack
FR9 - Agent.Shields
FR10 - Agent.PositionState
FR11 - Agent.Movement
FR12 - Movement.Direction
FR13 - Movement.Speed
'''
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