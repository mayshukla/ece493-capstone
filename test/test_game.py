import unittest

from src.game import *

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_exec_player_code_good(self):
        player_code = """
class MyAgent(Agent):
    def foo(self, x):
        return x + 1
        """
        success = self.game.exec_player_code(player_code, "MyAgent")
        assert(success)
        assert(self.game.agents[0].foo(100) == 101)

    def test_exec_player_code_wrong_name(self):
        player_code = """
class MyAgent(Agent):
    pass
        """
        success = self.game.exec_player_code(player_code, "asdfasdfasdf")
        assert(not success)

    def test_exec_player_code_no_class(self):
        player_code = """
1 + 1
        """
        success = self.game.exec_player_code(player_code, "MyAgent")
        assert(not success)


if __name__ == '__main__':
    unittest.main()