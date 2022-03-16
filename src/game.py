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
        self.agents = []

        for client in self.clients:
            def callback(client, code, class_name):
                print(self, client, code, class_name)
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
        try:
            # Compile in 'exec' mode since 'eval' mode doesn't allow class definitions.
            code = compile(player_code, 'Player Code', 'exec')
            # Make the Agent class in-scope to player code
            player_globals = {'Agent': Agent}
            exec(code, player_globals)
            # Get the class object so we can instantiate it later.
            # TODO what if both players have classes with the same name?
            agent_class = eval(class_name, player_globals)
            self.agents.append(agent_class())
            client.send_debug_message("Successfully created Agent instance from player code")
            return True
        except:
            client.send_debug_message("Failed to create Agent instance from player code")
            # TODO send error message to client to be printed on the actual page (not just console)
            return False
