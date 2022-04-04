import unittest
from unittest.mock import MagicMock
import math
from time import time
import sys

from src.game import *
from src.vector2 import Vector2

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game([])
        self.client = MagicMock()
        self.num_boundaries = 4

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
        self.game.physics.add_on_collision_callback(self.game.collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        obstacle = Obstacle(self.game.gen_id(), Vector2(100, 70), 30, 30)
        agent.on_obstacle_hit = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(0, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_obstacle(obstacle)
        self.game.physics.step(1)
        assert(agent.on_obstacle_hit.called)

    def test_damage_taken_callback(self):
        self.game.physics.add_on_collision_callback(self.game.collision_callback)
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
        self.game.physics.add_on_collision_callback(collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        obstacle = Obstacle(self.game.gen_id(), Vector2(200, 70), 30, 30)
        agent.on_obstacle_scanned = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(100, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_obstacle(obstacle)
        for _ in range(10):
            self.game.tick()
        collision_callback.assert_not_called()
        agent.on_obstacle_scanned.assert_called_with(obstacle)

    def test_enemy_scanned_callback(self):
        collision_callback = MagicMock()
        self.game.physics.add_on_collision_callback(collision_callback)
        agent = Agent(self.game.gen_id(), self.game)
        enemy = Agent(self.game.gen_id(), self.game)
        agent.on_enemy_scanned = MagicMock()
        self.game.agents = [[MagicMock(), agent]]
        agent._set_position(Vector2(200, 100))
        agent.agent_state.velocity = Vector2(100, 0)
        enemy._set_position(Vector2(300, 100))
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_agent(enemy.agent_state)
        for _ in range(10):
            self.game.tick()
        collision_callback.assert_not_called()
        agent.on_enemy_scanned.assert_called_with(enemy.get_position())

    def test_attack(self):
        attacker = Agent(self.game.gen_id(), self.game)
        attackee = Agent(self.game.gen_id(), self.game)
        attacker._set_position(Vector2(100, 800))
        attackee._set_position(Vector2(200, 800))
        attacker.game = self.game
        attackee.game = self.game

        self.game.agents = [[MagicMock(), attacker], [MagicMock(), attackee]]
        for agent in self.game.agents:
            self.game.physics.add_agent(agent[1].agent_state)

        attacker.attack_ranged(0)

        for _ in range(TICKS_PER_SECOND * 30):
            self.game.tick()

        self.assertEqual(attacker.get_health(), Agent.MAX_HEALTH)
        self.assertEqual(attackee.get_health(), Agent.MAX_HEALTH - Agent.DAMAGE_AMOUNT)

        # Ensure projectile destroyed
        self.assertEqual(len(self.game.physics.bodies), 2 + self.num_boundaries)

    def test_attack_shielded(self):
        attacker = Agent(self.game.gen_id(), self.game)
        attackee = Agent(self.game.gen_id(), self.game)
        attacker._set_position(Vector2(100, 800))
        attackee._set_position(Vector2(200, 800))
        attacker.game = self.game
        attackee.game = self.game

        self.game.agents = [[MagicMock(), attacker], [MagicMock(), attackee]]
        for agent in self.game.agents:
            self.game.physics.add_agent(agent[1].agent_state)

        attackee.activate_shield()
        attacker.attack_ranged(0)

        for _ in range(TICKS_PER_SECOND * 10):
            self.game.tick()

        self.assertEqual(attacker.get_health(), Agent.MAX_HEALTH)
        self.assertEqual(attackee.get_health(), Agent.MAX_HEALTH)

        # Ensure projectile destroyed
        self.assertEqual(len(self.game.physics.bodies), 2 + self.num_boundaries)

    def test_attack_cooldown(self):
        attacker = Agent(self.game.gen_id(), self.game)
        attackee = Agent(self.game.gen_id(), self.game)
        attacker._set_position(Vector2(100, 800))
        attackee._set_position(Vector2(200, 800))
        attacker.game = self.game
        attackee.game = self.game

        self.game.agents = [[MagicMock(), attacker], [MagicMock(), attackee]]
        for agent in self.game.agents:
            self.game.physics.add_agent(agent[1].agent_state)

        attacker.attack_ranged(0)
        attacker.attack_ranged(0)

        for _ in range(TICKS_PER_SECOND * 10):
            self.game.tick()

        self.assertEqual(attacker.get_health(), Agent.MAX_HEALTH)
        # Ensure damage was only taken once
        self.assertEqual(attackee.get_health(), Agent.MAX_HEALTH - Agent.DAMAGE_AMOUNT)

        # Attack cooldown period should have ended by now
        attacker.attack_ranged(0)
        for _ in range(TICKS_PER_SECOND * 10):
            self.game.tick()

        self.assertEqual(attacker.get_health(), Agent.MAX_HEALTH)
        self.assertEqual(attackee.get_health(), Agent.MAX_HEALTH - 2 * Agent.DAMAGE_AMOUNT)

        # Ensure projectile destroyed
        self.assertEqual(len(self.game.physics.bodies), 2 + self.num_boundaries)

    def test_attack_movement_speed(self):
        attacker = Agent(self.game.gen_id(), self.game)
        self.game.agents = [[MagicMock(), attacker], [MagicMock(), MagicMock()]]

        self.game.prepare_to_start_simulation()

        attacker.set_movement_speed(Agent.MAX_SPEED)
        self.assertAlmostEqual(attacker.agent_state.velocity.get_magnitude(), Agent.MAX_SPEED)
        attacker.attack_ranged(0)
        self.assertAlmostEqual(attacker.agent_state.velocity.get_magnitude(), Agent.MAX_SPEED_DURING_ATTACK)

        # Wait for cooldown
        for _ in range(TICKS_PER_SECOND * math.ceil(Agent.ATTACK_COOLDOWN_MAX)):
            self.game.tick()

        attacker.set_movement_speed(Agent.MAX_SPEED)
        self.assertAlmostEqual(attacker.agent_state.velocity.get_magnitude(), Agent.MAX_SPEED)

    def test_boundaries_stop_movement(self):
        agent = Agent(self.game.gen_id(), self.game)
        agent2 = Agent(self.game.gen_id(), self.game)
        self.game.agents = [[MagicMock(), agent], [MagicMock(), agent2]]
        agent._set_position(Vector2(500, 500))
        agent2._set_position(Vector2(100, 100))
        self.game.physics.add_agent(agent.agent_state)
        self.game.physics.add_agent(agent2.agent_state)

        agent.agent_state.velocity = Vector2(600, 0)
        for _ in range(30):
            self.game.tick()
        self.assertLessEqual(agent.agent_state.position.x, self.game.physics.SPACE_WIDTH)
        agent.agent_state.velocity = Vector2(-2000, 0)
        for _ in range(30):
            self.game.tick()
        self.assertGreaterEqual(agent.agent_state.position.x, 0)
        agent.agent_state.velocity = Vector2(0, 2000)
        for _ in range(30):
            self.game.tick()
        self.assertLessEqual(agent.agent_state.position.y, self.game.physics.SPACE_HEIGHT)
        agent.agent_state.velocity = Vector2(0, -2000)
        for _ in range(30):
            self.game.tick()
        self.assertGreaterEqual(agent.agent_state.position.y, 0)

    def test_destroy_projectile_message(self):
        attacker = Agent(self.game.gen_id(), self.game)
        attackee = Agent(self.game.gen_id(), self.game)
        attacker._set_position(Vector2(100, 800))
        attackee._set_position(Vector2(200, 800))
        attacker.game = self.game
        attackee.game = self.game

        self.game.agents = [[MagicMock(), attacker], [MagicMock(), attackee]]
        for agent in self.game.agents:
            self.game.physics.add_agent(agent[1].agent_state)

        attacker.attack_ranged(0)

        for _ in range(TICKS_PER_SECOND * 10):
            self.game.tick()

        for agent in self.game.agents:
            agent[0].send_destroy_message.assert_called_with(2, "projectile")

    def test_destroy_agent_message(self):
        attacker = Agent(self.game.gen_id(), self.game)
        attackee = Agent(self.game.gen_id(), self.game)
        attacker._set_position(Vector2(100, 800))
        attackee._set_position(Vector2(200, 800))
        attacker.game = self.game
        attackee.game = self.game

        self.game.agents = [[MagicMock(), attacker], [MagicMock(), attackee]]
        for agent in self.game.agents:
            self.game.physics.add_agent(agent[1].agent_state)
        
        self.game.game_start_time = time()

        # Perform enough attacks to eliminate attackee
        for _ in range(math.ceil(Agent.MAX_HEALTH / Agent.DAMAGE_AMOUNT)):
            attacker.attack_ranged(0)

            for _ in range(TICKS_PER_SECOND * 10):
                self.game.tick()

        for agent in self.game.agents:
            agent[0].send_destroy_message.assert_called_with(1, "agent")

    def test_player_exception_handling(self):
        exception = Exception()
        class MyAgent(Agent):
            def run(self):
                raise exception
        player = MyAgent(self.game.gen_id(), self.game)

        client = MagicMock()
        self.game.agents = [[client, player], [MagicMock(), MagicMock()]]

        self.game.prepare_to_start_simulation()

        self.game.tick()

        print(sys.exc_info())

        client.send_python_error.assert_called()


if __name__ == '__main__':
    unittest.main()