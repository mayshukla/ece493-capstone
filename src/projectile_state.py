'''
Class that represents projectiles in the game.

Part of the implementation of the following requirement:
FR8 - Agent.RangedAttack
'''

from src.dynamic_object_state import DynamicObjectState

class ProjectileState(DynamicObjectState):
    """Extends DynamicObjectState for projectiles."""

    def __init__(self, id, position, velocity, attackerId):
        """Constructor

        Arguments:
            id: unique int id
            position: a vector2 object representing the location of the center of the object.
            velocity: a vector2 object representing the object's velocity.
            attackerId: the id of the agent that fired the projectile.
        """
        super().__init__(id, position, velocity)
        self.attackerId = attackerId

    def to_json_dict(self):
        json_dict = {
            'id': self.id,
            'position': {'x': self.position.x, 'y': self.position.y},
            'velocity': {'x': self.velocity.x, 'y': self.velocity.y},
            'angle': self.velocity.get_angle(),
            'attackerId': self.attackerId,
        }
        return json_dict