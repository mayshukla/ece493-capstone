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
    ATTACK_COOLDOWN_MAX = 0.5
    TIMER_DECREMENT = 1 / TICKS_PER_SECOND
    SCAN_DISTANCE = 50
    MAX_SPEED = 50 # in units of pixels per second
    MAX_SPEED_DURING_ATTACK = MAX_SPEED * 0.5
    PROJECTILE_SPEED = 200

    def __init__(self, id, game):
        self.agent_state = AgentState(
            id,
            Vector2(0, 0),
            Vector2(0, 0),
            Agent.MAX_HEALTH
        )
        self.shield_timer = Timer(Agent.SHIELD_TIME_MAX, Agent.SHIELD_TIME_MAX, callback=self.deactivate_shield)
        self.shield_cooldown_timer = Timer(Agent.SHIELD_COOLDOWN_MAX, 0)
        self.attack_cooldown_timer = Timer(Agent.ATTACK_COOLDOWN_MAX, 0)

        self.game = game

        # Dict to map any objects that are colliding with this agent to the point at which they have collided.
        self.collisions = {}

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
        if self.get_shield_cooldown_time() > 0:
            return
        self.agent_state.shieldEnabled = True
        self.shield_cooldown_timer.reset()

    def deactivate_shield(self):
        """Activates the agent's shield if it is activated."""
        if not self.agent_state.shieldEnabled:
            return
        self.agent_state.shieldEnabled = False
        self.shield_timer.reset()

    def get_shield_time(self):
        return self.shield_timer.get_time()

    def get_shield_cooldown_time(self):
        return self.shield_cooldown_timer.get_time()

    def attack_ranged(self, direction):
        """Triggers a ranged attack in the specified direction.

        If within the cooldown period, this function does nothing.
        The cooldown period is defined by Agent.ATTACK_COOLDOWN_MAX

        Args:
            direction: Direction in degrees. Follows same angle convection as
                set_movement_direction.
        """
        if self.attack_cooldown_timer.get_time() > 0:
            return

        self.attack_cooldown_timer.reset()

        self.game.create_projectile(
            self.agent_state.position.clone(),
            direction,
            self.agent_state.id
        )

        # Limit max speed
        if self.agent_state.velocity.get_magnitude() > Agent.MAX_SPEED_DURING_ATTACK:
            self.set_movement_speed(Agent.MAX_SPEED_DURING_ATTACK)

    def set_movement_speed(self, speed):
        """Sets the current speed of the agent in units of pixels per second.

        If a speed greater that Agent.MAX_SPEED is given, then the speed is set
        to Agent.MAX_SPEED.

        If the agent is currently within the attack cooldown period, then the
        speed is clamped at Agent.MAX_SPEED_DURING_ATTACK.

        Args:
            speed: Desired speed in units of pixels per second.
        """
        max_speed = Agent.MAX_SPEED
        if self.attack_cooldown_timer.get_time() > 0:
            max_speed = Agent.MAX_SPEED_DURING_ATTACK

        angle = self.agent_state.velocity.get_angle()
        magnitude = speed if speed <= max_speed else max_speed
        self.agent_state.velocity = Vector2.from_angle_magnitude(angle, magnitude)
        #print(self.agent_state.velocity)

    def _clip_velocity(self):
        """
        Sets the agent's velocity to 0 if their current velocity would cause them to clip through an object they are colliding with.
        """
        for collision, contact_point in self.collisions.items():
            if abs(contact_point.y - self.get_position().y) >= AGENT_RADIUS:
                if contact_point.y < self.get_position().y:
                    if self.agent_state.velocity.y < 0:
                        self.agent_state.velocity.x = 0
                        self.agent_state.velocity.y = 0
                    # print("y must be positive")
                    # print("contact at: " + str(self.collisions[collision].y))
                    # print("current pos: " + str(self.get_position().y))
                elif contact_point.y > self.get_position().y:
                    if self.agent_state.velocity.y > 0:
                        self.agent_state.velocity.x = 0
                        self.agent_state.velocity.y = 0
                    # print("y must be negative")
                    # print("contact at: " + str(self.collisions[collision].y))
                    # print("current pos: " + str(self.get_position().y))
            if abs(contact_point.x - self.get_position().x) >= AGENT_RADIUS:
                if contact_point.x < self.get_position().x:
                    if self.agent_state.velocity.x < 0:
                        self.agent_state.velocity.x = 0
                        self.agent_state.velocity.y = 0
                    # print("x must be positive")
                    # print("contact at: " + str(self.collisions[collision].x))
                    # print("current pos: " + str(self.get_position().x))
                elif contact_point.x > self.get_position().x:
                    if self.agent_state.velocity.x > 0:
                        self.agent_state.velocity.x = 0
                        self.agent_state.velocity.y = 0
                    # print("x must be negative")
                    # print("contact at: " + str(self.collisions[collision].x))
                    # print("current pos: " + str(self.get_position().x))

        # print("after: " + str(self.agent_state.velocity.x) + ", " + str(self.agent_state.velocity.y))
        return self.agent_state.velocity

    def set_movement_direction(self, angle):
        """Sets the current direction of movement.

        The direction is specified in units of degrees.
        Zero degrees means directly to the right.
        Positive angles turn the agent clockwise from the zero degree position.

        Args:
            angle: Desired angle in degrees.
        """
        # print("setting angle: " + str(angle))
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

    def _add_collision(self, colliding_object_state, collision_point):
        """
        Adds an object that is currently colliding with this agent.

        Arguments:
            collising_object_state: the object_state that has collided with this agent.
            collision_point: The approximate coordinates at which the object and this agent collided.
        """
        self.collisions[colliding_object_state] = collision_point

    def _remove_collision(self, colliding_object_state):
        """
        Removes an object that is no longer colliding with this agent.

        Arguments:
            collising_object_state: the object_state that is no longer colliding with this agent.
        """
        self.collisions.pop(colliding_object_state)

    def _tick(self):
        """Main interface for game loop.

        Performs all the functions that need to be done in one iteration of the
        game loop such as decrementing timers.
        """
        if self.agent_state.shieldEnabled:
            self.shield_timer.tick()
        else:
            self.shield_cooldown_timer.tick()
        self.attack_cooldown_timer.tick()

        self.run()
        self._clip_velocity()

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

class Timer():
    """Timer"""
    def __init__(self, max_time, initial_time, callback=None):
        self.callback = callback
        self.max_time = max_time
        self.time = initial_time

    def get_time(self):
        return self.time

    def reset(self):
        self.time = self.max_time

    def tick(self):
        if self.time > 0:
            self.time -= Agent.TIMER_DECREMENT
        if self.time < 0:
            self.time = 0
        if self.time == 0:
            if self.callback is not None:
                self.callback()