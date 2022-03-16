from src.agent import Agent

class Game():
    """Represents a single game.

    In charge of game logic and detecting end condition.
    """
    def __init__(self):
        self.agent_classes = []

    def exec_player_code(self, player_code, class_name):
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
            self.agent_classes.append(agent_class)
            return True
        except:
            # TODO send error message to client to be printed
            return False
