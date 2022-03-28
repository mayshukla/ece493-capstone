import unittest
from unittest.mock import MagicMock

from src.game import *
from src.vector2 import Vector2

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
            agent_mock[1]._tick.assert_called()

        # TODO add more asserts as we add functionality to Game.tick

    def test_obstacle_hit_callback(self):
        self.game.physics.addOnCollisionCallback(self.game.collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        obstacle = Obstacle(self.game.gen_id(), Vector2(100, 70), 30, 30)
        agent.on_obstacle_hit = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(0, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_obstacle(obstacle)
        self.game.physics.step(2)
        assert(agent.on_obstacle_hit.called)

    def test_damage_taken_callback(self):
        self.game.physics.addOnCollisionCallback(self.game.collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        projectile = ProjectileState(self.game.gen_id(), Vector2(0, 100), Vector2(100, 0), self.game.gen_id())
        agent.on_damage_taken = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(100, 100))
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_projectile(projectile)
        self.game.physics.step(1)
        assert(agent.on_damage_taken.called)

    def test_obstacle_scanned_callback(self):
        collision_callback = MagicMock()
        self.game.physics.addOnCollisionCallback(collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        obstacle = Obstacle(self.game.gen_id(), Vector2(100, 70), 30, 30)
        agent.on_obstacle_scanned = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(0, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_obstacle(obstacle)
        for i in range(40):
            self.game.tick()
        collision_callback.assert_not_called()
        agent.on_obstacle_scanned.assert_called_with(obstacle)

    def test_enemy_scanned_callback(self):
        collision_callback = MagicMock()
        self.game.physics.addOnCollisionCallback(collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        enemy = Agent(self.game.gen_id(), self.game)
        agent.on_enemy_scanned = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(0, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        enemy._set_position(Vector2(100, 100))
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_agent(enemy.agent_state)
        for i in range(10):
            self.game.tick()
        collision_callback.assert_not_called()
        agent.on_enemy_scanned.assert_called_with(enemy.get_position())


        



if __name__ == '__main__':
    unittest.main()