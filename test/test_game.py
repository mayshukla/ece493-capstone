import unittest
from unittest.mock import MagicMock

from src.game import *

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game([])
        self.client = MagicMock()

    def mock_agents(self):
        self.game.agents = [MagicMock(), MagicMock()]

    def test_exec_player_code_good(self):
        player_code = """
class MyAgent(Agent):
    def foo(self, x):
        return x + 1
        """
        success = self.game.exec_player_code(self.client, player_code, "MyAgent")
        assert(success)
        assert(self.game.agents[0][1].foo(100) == 101)

    def test_exec_player_code_wrong_name(self):
        player_code = """
class MyAgent(Agent):
    pass
        """
        success = self.game.exec_player_code(self.client, player_code, "asdfasdfasdf")
        assert(not success)

    def test_exec_player_code_no_class(self):
        player_code = """
1 + 1
        """
        success = self.game.exec_player_code(self.client, player_code, "MyAgent")
        assert(not success)

    def test_tick(self):
        self.mock_agents()
        self.game.tick()
        for agent_mock in self.game.agents:
            agent_mock._tick.assert_called()

        # TODO add more asserts as we add functionality to Game.tick


if __name__ == '__main__':
    unittest.main()