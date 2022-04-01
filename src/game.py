import asyncio

import tornado.ioloop

from src.agent import Agent
from src.physics_engine import PhysicsEngine
from src.globals import *
from src.projectile_state import ProjectileState
from src.agent_state import AgentState
from src.obstacle import Obstacle
from src.vector2 import Vector2
from time import time
import sys

PLAYABLE_AREA_X_MIN = 65
PLAYABLE_AREA_X_MAX = 1024 - PLAYABLE_AREA_X_MIN
PLAYABLE_AREA_Y_MIN = 25
PLAYABLE_AREA_Y_MAX = 700 - PLAYABLE_AREA_Y_MIN

class Game():
    """Represents a single game.

    In charge of game logic and detecting end condition.
    """

    def __init__(self, clients):
        """Constructor

        Args:
            clients: List of ServerToClientConnection instances.
        """
        self.clients = clients
        # List of pairs [client, agent]
        self.agents = []
        self.simulation_started = False

        self.next_id = 0

        self.physics = PhysicsEngine()
        self.physics.add_on_collision_callback(self.collision_callback)
        self.physics.add_on_separate_callback(self.separate_callback)

        for client in self.clients:
            def callback(client, code, class_name):
                self.exec_player_code(client, code, class_name)
            client.on_receive_player_code = callback

        self.projectiles = []

        self.game_start_time = None

        # True if there was an error in player code.
        self.player_error = False

    async def run_game_loop(self):
        """Continuously steps physics engine and updates clients"""
        self.prepare_to_start_simulation()
        self.game_start_time = time()

        while True:
            game_ended = self.tick()

            if self.player_error:
                tie = True
                for agent in self.agents:
                    if not agent[1].had_error:
                        tie = False
                for agent in self.agents:
                    winner = False
                    if not agent[1].had_error:
                        winner = True
                    agent[0].send_results(winner, tie, self.agents, error=True)
                return

            if game_ended:
                tie = True
                for agent in self.agents:
                    if agent[1].get_health() > 0:
                        tie = False
                for agent in self.agents:
                    winner = False
                    if agent[1].get_health() > 0:
                        winner = True
                    agent[0].send_results(winner, tie, self.agents)
                return
            await asyncio.sleep(1 / TICKS_PER_SECOND)

    def tick(self):
        """Performs one iteration of game loop

        Returns:
            True if game end condition has been reached.
            False otherwise.
        """
        game_ended = False

        self.physics.step(1 / TICKS_PER_SECOND)
        for agent in self.agents:
            self.run_player_defined_method(agent[1], lambda: agent[1]._tick(), agent[0])

        # determine if agents have scanned anything
        for agent in self.agents:
            scanned_objects = self.physics.scan_area(agent[1].get_position(), Agent.SCAN_DISTANCE)
            # call appropriate callback for each scanned object
            for object in scanned_objects:
                if object == agent[1].agent_state:
                    continue
                elif isinstance(object, AgentState):
                    self.run_player_defined_method(agent[1], lambda: agent[1].on_enemy_scanned(object.position), agent[0])
                elif isinstance(object, Obstacle):
                    self.run_player_defined_method(agent[1], lambda: agent[1].on_obstacle_scanned(object), agent[0])

        # check if an agent has been eliminated
        for agent in self.agents:
            if agent[1].get_health() != 0:
                continue
            # TODO do we need to handle both agents reaching 0 health in the
            # same tick?
            game_ended = True
            agent[1].survival_time = time() - self.game_start_time
            destroyed_id = agent[1].agent_state.id
            for agent in self.agents:
                agent[0].send_destroy_message(destroyed_id, "agent")

        # send updates to clients
        for agent in self.agents:
            #print(agent[1].agent_state.position)
            agent[0].send_agent_states([agent[1].agent_state for agent in self.agents])
            agent[0].send_projectile_states([projectile for projectile in self.projectiles])

        return game_ended

    def prepare_to_start_simulation(self):
        """Does setup work that needs to be done after all agents are created but before game loop starts.

        - Sets starting positions of agents and obstacles.
        - Initializes physics engine
        """
        # TODO figure out what starting positions should be
        self.agents[0][1]._set_position(Vector2(PLAYABLE_AREA_X_MIN + 65, 350))
        self.agents[0][1].set_movement_direction(0)
        self.agents[1][1]._set_position(Vector2(PLAYABLE_AREA_X_MAX - 65, 350))
        self.agents[1][1].set_movement_direction(180)

        # TODO set obstacle positions and add to physics

        # left obstacles
        init_x = PLAYABLE_AREA_X_MIN + 65
        init_y = 350 + 200
        self.physics.add_obstacle(Obstacle(self.gen_id(), Vector2(init_x, init_y), 32, 32))


        for agent in self.agents:
            self.physics.add_agent(agent[1].agent_state)

    def collision_callback(self, object_state_1, object_state_2, contact_point):
        """Callback for when physics engine detects collision."""
        if isinstance(object_state_1, ProjectileState) and isinstance(object_state_2, ProjectileState):
            # handle projectile-projectile collision
            # destroy both projectiles
            self.physics.remove_object(object_state_1.id)
            self.physics.remove_object(object_state_2.id)
            self.projectiles.remove(object_state_1)
            self.projectiles.remove(object_state_2)
            for agent in self.agents:
                    agent[0].send_destroy_message(object_state_1.id, "projectile")
                    agent[0].send_destroy_message(object_state_2.id, "projectile")
        elif isinstance(object_state_1, AgentState) and isinstance(object_state_2, AgentState):
            pass
        elif isinstance(object_state_1, ProjectileState) or isinstance(object_state_2, ProjectileState):
            if isinstance(object_state_1, AgentState) or isinstance(object_state_2, AgentState):
                # handle projectile-agent collision
                if isinstance(object_state_1, AgentState):
                    agent = self.get_agent_from_state(object_state_1)
                    client = self.get_client_from_state(object_state_1)
                    projectile = object_state_2
                else:
                    agent = self.get_agent_from_state(object_state_2)
                    client = self.get_client_from_state(object_state_2)
                    projectile = object_state_1
                # damage the agent if their shields are not active
                if not agent.is_shield_activated():
                    agent._decrement_health()
                    # callback
                    self.run_player_defined_method(agent, lambda: agent.on_damage_taken(), client)
                # remove the projectile
                self.physics.remove_object(projectile.id)
                self.projectiles.remove(projectile)
                for agent in self.agents:
                    agent[0].send_destroy_message(projectile.id, "projectile")
            else:
                # handle projectile-obstacle collision
                if isinstance(object_state_1, ProjectileState):
                    projectile = object_state_1
                else:
                    projectile = object_state_2
                # remove the projectile
                self.physics.remove_object(projectile.id)
                self.projectiles.remove(projectile)
                for agent in self.agents:
                    agent[0].send_destroy_message(projectile.id, "projectile")
        else:
            # handle agent-obstacle collision
            if isinstance(object_state_1, AgentState):
                agent = self.get_agent_from_state(object_state_1)
                client = self.get_client_from_state(object_state_1)
                obstacle = object_state_2
            else:
                agent = self.get_agent_from_state(object_state_2)
                client = self.get_client_from_state(object_state_2)
                obstacle = object_state_1
            # callback
            agent._add_collision(obstacle, contact_point)
            self.run_player_defined_method(agent, lambda: agent.on_obstacle_hit(), client)
            agent.on_obstacle_hit()

    def separate_callback(self, object_state_1, object_state_2):
        """Callback for when physics engine detects that two colliding objects have now separated."""
        if isinstance(object_state_1, AgentState) or isinstance(object_state_2, AgentState):
            if isinstance(object_state_1, Obstacle) or isinstance(object_state_2, Obstacle):
                # handle agent-obstacle separation
                if isinstance(object_state_1, AgentState):
                    agent = self.get_agent_from_state(object_state_1)
                    obstacle = object_state_2
                else:
                    agent = self.get_agent_from_state(object_state_2)
                    obstacle = object_state_1
                agent._remove_collision(obstacle)

    def get_agent_from_state(self, agent_state):
        """Returns the agent that corresponds to the agent_state.
        Returns None if the agent cannot be found."""
        for agent in self.agents:
            if agent[1].agent_state.id == agent_state.id:
                return agent[1]
        return None

    def get_client_from_state(self, agent_state):
        """Returns the client that corresponds to the agent_state.
        Returns None if the client cannot be found."""
        for agent in self.agents:
            if agent[1].agent_state.id == agent_state.id:
                return agent[0]
        return None

    def exec_player_code(self, client, player_code, class_name):
        """Attempts to execute player code and get the the agent class created
        by the player.

        Args:
            player_code: Code input from player as string.
            class_name: The name of the Agent subclass created by the player.
        Returns:
            True on success. False otherwise
        """
        if self.simulation_started:
            message = "ERROR: client sent code after simulation started."
            print(message)
            client.send_debug_message(message)
            return

        try:
            # Compile in 'exec' mode since 'eval' mode doesn't allow class definitions.
            code = compile(player_code, 'Player Code', 'exec')
            # Make the Agent class in-scope to player code
            player_globals = {'Agent': Agent}
            exec(code, player_globals)
            # Get the class object so we can instantiate it later.
            # TODO what if both players have classes with the same name?
            class_name = class_name.strip()
            agent_class = eval(class_name, player_globals)

            # Check if player has already submitted code and if so, replace
            # agent instead of appending.
            agent_instance = agent_class(self.gen_id(), self)
            agent_index = self.get_index_of_client_agent(client)
            if agent_index is not None:
                self.agents[agent_index][1] = agent_instance
                client.send_debug_message("Successfully updated Agent instance from player code")
            else:
                self.agents.append([client, agent_instance])
                client.send_debug_message("Successfully created Agent instance from player code")

            # Check if both clients have submitted valid code and if so, start the simulation.
            if len(self.agents) == 2:
                self.simulation_started = True

                for client in self.clients:
                    client.send_start_simulation_message()

                # call run_game_loop at the next iteration of the i/o loop
                tornado.ioloop.IOLoop.current().add_callback(self.run_game_loop)

            return True
        except Exception as e:
            client.send_debug_message("Failed to create Agent instance from player code")
            e_type, e_value, e_traceback = sys.exc_info()
            client.send_python_error(e_type, e_value, e_traceback)
            return False

    def get_index_of_client_agent(self, client):
        """
        Args:
            client: ServerToClientConnection index.
        Returns:
            Index into self.agents that has a matching client.
            Returns None if there is no agent that matches the given client.
        """
        for i in range(len(self.agents)):
            if self.agents[i][0] == client:
                return i

        return None

    def gen_id(self):
        """Generates a new unique ID with each call
        """
        _id = self.next_id
        self.next_id += 1
        return _id

    def get_agents(self):
        return self.agents

    def create_projectile(self, position, direction, attackerId):
        """Creates a new projectile and passes it to the physics engine."""
        velocity = Vector2.from_angle_magnitude(direction, Agent.PROJECTILE_SPEED)

        projectile_state = ProjectileState(
            self.gen_id(),
            position,
            velocity,
            attackerId
        )

        self.projectiles.append(projectile_state)

        self.physics.add_projectile(projectile_state)

    def run_player_defined_method(self, agent, method, client):
        """Runs a player-defined method such as Agent.run() with proper error
        handling.

        Exceptions are caught and sent to the client.
        """

        try:
            method()
        except Exception as e:
            e_type, e_value, e_traceback = sys.exc_info()
            client.send_python_error(e_type, e_value, e_traceback)
            agent.had_error = True
            self.player_error = True
