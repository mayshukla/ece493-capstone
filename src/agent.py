from src.agent_state import AgentState
from src.game import Game
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
    SHIELD_TIME_MAX = 10
    SHIELD_COOLDOWN_MAX = 20
    TIMER_DECREMENT = 1 / Game.TICKS_PER_SECOND

    def __init__(self, id, game):
        self.agent_state = AgentState(
            id,
            Vector2(0, 0),
            Vector2(0, 0),
            Agent.MAX_HEALTH
        )
        self.shield_time = Agent.SHIELD_TIME_MAX
        self.shield_cooldown_time = Agent.SHIELD_COOLDOWN_MAX

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

    def is_shield_activated(self):
        """Returns true if shield is activated."""
        return self.agent_state.shieldEnabled

    def activate_shield(self):
        """Activates the agent's shield if it is allowed to do so."""
        if self.agent_state.shieldEnabled:
            return
        if self.shield_cooldown_time > 0:
            return
        self.agent_state.shieldEnabled = True
        self.shield_cooldown_time = Agent.SHIELD_COOLDOWN_MAX

    def deactivate_shield(self):
        """Activates the agent's shield if it is activated."""
        if not self.agent_state.shieldEnabled:
            return
        self.agent_state.shieldEnabled = False
        self.shield_time = Agent.SHIELD_TIME_MAX

    def get_shield_time(self):
        return self.shield_time

    def get_shield_cooldown_time(self):
        return self.shield_cooldown_time

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

    def _tick(self):
        """Decrements timers. This is called in the game loop."""
        if self.agent_state.shieldEnabled:
            if self.shield_time > 0:
                self.shield_time -= Agent.TIMER_DECREMENT
            if self.shield_time <= 0:
                self.deactivate_shield()
        else:
            if self.shield_cooldown_time > 0:
                self.shield_cooldown_time -= Agent.TIMER_DECREMENT