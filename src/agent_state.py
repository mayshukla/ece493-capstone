'''
Class that represents that state of agents within the game.

Part of the implementation of the following requirements:
FR7 - Agent.HealthState
FR9 - Agent.Shields
FR10 - Agent.PositionState
FR11 - Agent.Movement
FR12 - Movement.Direction
FR13 - Movement.Speed
'''
from src.dynamic_object_state import DynamicObjectState

class AgentState(DynamicObjectState):
    """Extends DynamicObjectState for agents."""

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
        self.angle = velocity.get_angle()

    def to_json_dict(self):
        json_dict = {
            'id': self.id,
            'position': {'x': self.position.x, 'y': self.position.y},
            'velocity': {'x': self.velocity.x, 'y': self.velocity.y},
            'angle': self.angle,
            'health': self.health,
            'shieldEnabled': self.shieldEnabled
        }
        return json_dict