import unittest

from src.game import *
from src.vector2 import Vector2

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(0)

    def test_get_health(self):
        assert(self.agent.get_health() == Agent.MAX_HEALTH)
        self.agent._decrement_health()
        expected_health = Agent.MAX_HEALTH - Agent.DAMAGE_AMOUNT
        assert(self.agent.get_health() == expected_health)

    def test_get_position(self):
        expected_position = Vector2(0, 0)
        assert(self.agent.get_position() == expected_position)
        expected_position = Vector2(6.7, 3.2)
        self.agent._set_position(expected_position)
        assert(self.agent.get_position() == expected_position)


if __name__ == '__main__':
    unittest.main()