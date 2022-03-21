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
            'velocity': {'x': str(self.velocity.x), 'y': self.velocity.y},
            'attackerId': self.attackerId,
        }
        return json_dict

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
            'velocity': {'x': str(self.velocity.x), 'y': self.velocity.y},
            'health': self.health,
            'shieldEnabled': self.shieldEnabled
        }
        return json_dict