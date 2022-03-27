from src.agent_state import AgentState
from src.vector2 import Vector2
from src.globals import *

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
    TIMER_DECREMENT = 1 / TICKS_PER_SECOND
    SCAN_DISTANCE = 50
    MAX_SPEED = 50 # in units of pixels per second
    PROJECTILE_SPEED = 200

    def __init__(self, id, game):
        self.agent_state = AgentState(
            id,
            Vector2(0, 0),
            Vector2(0, 0),
            Agent.MAX_HEALTH
        )
        self.shield_time = Agent.SHIELD_TIME_MAX
        self.shield_cooldown_time = 0

        self.game = game

    def run(self):
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

    def attack_ranged(self, direction):
        """Triggers a ranged attack in the specified direction.

        Args:
            direction: Direction in degrees. Follows same angle convection as
                set_movement_direction.
        """
        # TODO implement attack cooldown
        self.game.create_projectile(
            self.agent_state.position.clone(),
            direction,
            self.agent_state.id
        )

    def set_movement_speed(self, speed):
        """Sets the current speed of the agent in units of pixels per second.

        If a speed greater that Agent.MAX_SPEED is given, then the speed is set
        to Agent.MAX_SPEED.

        Args:
            speed: Desired speed in units of pixels per second.
        """
        angle = self.agent_state.velocity.get_angle()
        magnitude = speed if speed <= Agent.MAX_SPEED else Agent.MAX_SPEED
        self.agent_state.velocity = Vector2.from_angle_magnitude(angle, magnitude)

    def set_movement_direction(self, angle):
        """Sets the current direction of movement.

        The direction is specified in units of degrees.
        Zero degrees means directly to the right.
        Positive angles turn the agent clockwise from the zero degree position.

        Args:
            angle: Desired angle in degrees.
        """
        magnitude = self.agent_state.velocity.get_magnitude()
        self.agent_state.velocity = Vector2.from_angle_magnitude(angle, magnitude)

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
        """Main interface for game loop.

        Performs all the functions that need to be done in one iteration of the
        game loop such as decrementing timers.
        """
        if self.agent_state.shieldEnabled:
            if self.shield_time > 0:
                self.shield_time -= Agent.TIMER_DECREMENT
            if self.shield_time <= 0:
                self.deactivate_shield()
        else:
            if self.shield_cooldown_time > 0:
                self.shield_cooldown_time -= Agent.TIMER_DECREMENT
            if self.shield_cooldown_time < 0:
                self.shield_cooldown_time = 0

        self.run()

    def on_enemy_scanned(self, enemy_position):
        """Callback that players can override. Called when an enemy is nearby."""
        pass

    def on_obstacle_scanned(self, obstacle):
        """Callback that players can override. Called when an obstacle is nearby."""
        pass

    def on_damage_taken(self):
        """Callback that players can override. Called when the agent is damaged by a projectile."""
        pass

    def on_obstacle_hit(self):
        """Callback that players can override. Called when the agent runs into an obstacle."""
        pass