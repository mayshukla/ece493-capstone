from src.agent import Agent

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

        for client in self.clients:
            def callback(client, code, class_name):
                self.exec_player_code(client, code, class_name)
            client.on_receive_player_code = callback

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
            agent_instance = agent_class()
            agent_index = self.get_index_of_client_agent(client)
            if agent_index is not None:
                self.agents[agent_index][1] = agent_instance
                client.send_debug_message("Successfully updated Agent instance from player code")
            else:
                self.agents.append([client, agent_class()])
                client.send_debug_message("Successfully created Agent instance from player code")

            # Check if both clients have submitted valid code and if so, start the simulation.
            if len(self.agents) == 2:
                self.simulation_started = True

                for client in self.clients:
                    client.send_start_simulation_message()

                # TODO start the physics engine

            return True
        except Exception as e:
            client.send_debug_message("Failed to create Agent instance from player code")
            client.send_python_error(e)
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
