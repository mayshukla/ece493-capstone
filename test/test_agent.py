import unittest
from unittest.mock import MagicMock

from src.game import *
from src.vector2 import Vector2

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.game = MagicMock()
        self.agent = Agent(0, self.game)
        self.enemy_agent = Agent(1, self.game)

        # Mock game.get_agents()
        agents = [self.agent, self.enemy_agent]
        self.game.get_agents = MagicMock(return_value=agents)

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

    def test_get_agents_position(self):
        expected_position = Vector2(8.9, 4.1)
        self.enemy_agent._set_position(expected_position)
        actual_positions = self.agent.get_agents_position()
        assert(len(actual_positions) == 1)
        assert(actual_positions[0] == expected_position)

    def test_get_agents_position(self):
        self.enemy_agent._decrement_health()
        expected_health = Agent.MAX_HEALTH - Agent.DAMAGE_AMOUNT
        actual_healths = self.agent.get_agents_health()
        assert(len(actual_healths) == 1)
        assert(actual_healths[0] == expected_health)

    def test_activate_shield(self):
        assert(not self.agent.is_shield_activated())
        self.agent.activate_shield()
        assert(self.agent.is_shield_activated())
        assert(self.agent.get_shield_time() == Agent.SHIELD_TIME_MAX)
        self.agent._tick()
        assert(self.agent.get_shield_time() == Agent.SHIELD_TIME_MAX - Agent.TIMER_DECREMENT)

        # Should do nothing when shield is already activated
        self.agent.activate_shield()
        assert(self.agent.get_shield_time() == Agent.SHIELD_TIME_MAX - Agent.TIMER_DECREMENT)

    def test_deactivate_shield(self):
        self.agent.activate_shield()
        self.agent.deactivate_shield()
        assert(not self.agent.is_shield_activated())
        assert(self.agent.get_shield_time() == Agent.SHIELD_TIME_MAX)
        assert(self.agent.get_shield_cooldown_time() == Agent.SHIELD_COOLDOWN_MAX)
        self.agent._tick()
        assert(self.agent.get_shield_cooldown_time() == Agent.SHIELD_COOLDOWN_MAX - Agent.TIMER_DECREMENT)

        # Should do nothing when shield is already activated
        self.agent.deactivate_shield()
        assert(self.agent.get_shield_cooldown_time() == Agent.SHIELD_COOLDOWN_MAX - Agent.TIMER_DECREMENT)

    def test_shield_timer(self):
        self.agent.activate_shield()
        for _ in range(Agent.SHIELD_TIME_MAX * TICKS_PER_SECOND + 1):
            self.agent._tick()
        assert(not self.agent.is_shield_activated())

    def test_shield_cooldown_timer(self):
        self.agent.activate_shield()
        self.agent.deactivate_shield()
        for _ in range(Agent.SHIELD_COOLDOWN_MAX * TICKS_PER_SECOND + 1):
            self.agent._tick()
        print(self.agent.get_shield_cooldown_time())
        assert(self.agent.get_shield_cooldown_time() == 0)


if __name__ == '__main__':
    unittest.main()