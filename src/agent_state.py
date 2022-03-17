from dynamic_object_state import DynamicObjectState

class AgentState(DynamicObjectState):
    """Extends DynamicObjectState for projectiles."""

    def __init__(self, id, position, velocity, health, shieldEnabled=False):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the object's location
            velocity: a vector2 object representing the object's velocity.
            health: the amount of health the agent should start with.
            shieldEnabled (optional): indicates whether the agent's shield will initially be enabled. False by default.
        """
        super().__init__(id, position, velocity)
        self.health = health
        self.shieldEnabled = shieldEnabled