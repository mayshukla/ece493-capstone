from src.agent_state import AgentState
from src.vector2 import Vector2

class Agent:
    """Base class for an Agent that should be extended by player code.

    Functions with names that don't start with underscores are part of the
    player API. E.g. run(), get_health()

    Functions with names that start with underscores should *not* be called from
    player code. E.g. _decrement_health()
    """

    MAX_HEALTH = 100
    DAMAGE_AMOUNT = 10

    def __init__(self, id, game):
        self.agent_state = AgentState(
            id,
            Vector2(0, 0),
            Vector2(0, 0),
            Agent.MAX_HEALTH
        )

        self.game = game

    def run():
        """This function will be called repeatedly in the main game loop.

        Players can override this function to implement agent behavior.
        """
        pass

    def get_health(self):
        """Gets health of agent

        Returns:
            Health as number between 0 and 100
        """
        return self.agent_state.health

    def get_position(self):
        """Gets current position of agent

        Example:
            position = self.get_position()
            x_position = position.x
            y_position = position.y

        Returns:
            Position as Vector2 (object with x and y fields).
        """
        return self.agent_state.position

    def get_agents_position(self):
        """Gets position of all agents except this agent.

        Returns:
            List of Vector2 objects representing positions.
        """
        positions = []
        agents = self.game.get_agents()
        for agent in agents:
            if agent.agent_state.id == self.agent_state.id:
                continue
            positions.append(agent.agent_state.position)
        return positions

    def get_agents_health(self):
        """Gets health of all agents except this agent.

        Returns:
            List of numbers representing health.
        """
        healths = []
        agents = self.game.get_agents()
        for agent in agents:
            if agent.agent_state.id == self.agent_state.id:
                continue
            healths.append(agent.agent_state.health)
        return healths

    def _set_position(self, position):
        """
        Args:
            position: New position as Vector2
        """
        self.agent_state.position = position

    def _decrement_health(self):
        """Decreases health by Agent.DAMAGE_AMOUNT
        """
        self.agent_state.health -= Agent.DAMAGE_AMOUNT