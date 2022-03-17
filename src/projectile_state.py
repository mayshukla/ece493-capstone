from dynamic_object_state import DynamicObjectState

class ProjectileState(DynamicObjectState):
    """Extends DynamicObjectState for projectiles."""

    def __init__(self, id, position, velocity, attackerId):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the object's location
            velocity (optional): a vector2 object representing the object's velocity. 0 by default.
            attackerId: the id of the agent that fired the projectile.
        """
        super().__init__(id, position, velocity)
        self.attackerId = attackerId