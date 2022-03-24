from src.dynamic_object_state import DynamicObjectState

class AgentState(DynamicObjectState):
    """Extends DynamicObjectState for projectiles."""

    def __init__(self, id, position, velocity, health, shieldEnabled=False):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the location of the center of the object.
            velocity: a vector2 object representing the object's velocity.
            health: the amount of health the agent should start with.
            shieldEnabled (optional): indicates whether the agent's shield will initially be enabled. False by default.
        """
        super().__init__(id, position, velocity)
        self.health = health
        self.shieldEnabled = shieldEnabled

    def to_json_dict(self):
        json_dict = {
            'id': self.id,
            'position': {'x': self.position.x, 'y': self.position.y},
            'velocity': {'x': self.velocity.x, 'y': self.velocity.y},
            'angle': self.velocity.get_angle(),
            'health': self.health,
            'shieldEnabled': self.shieldEnabled
        }
        return json_dict