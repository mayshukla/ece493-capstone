import unittest
from unittest.mock import MagicMock

from src.message import *
from src.physics_engine import *
from src.object_state import *
from src.agent_state import *
from src.obstacle import *
from src.projectile_state import *
from src.vector2 import *

class TestPhysicsEngine(unittest.TestCase):

    def setUp(self):
        print("starting...")
        self.pe = PhysicsEngine()
        self.callback = MagicMock()
        self.pe.addOnCollisionCallback(self.callback)

    def test_collision_callback(self):
        agent_state_1 = AgentState(1, Vector2(100, 200), Vector2(5, 0), 10)
        agent_state_2 = AgentState(2, Vector2(300, 200), Vector2(0, 0), 10)
        self.pe.add_agent(agent_state_1)
        self.pe.add_agent(agent_state_2)
        self.pe.step(40)
        self.callback.assert_called_with(agent_state_1, agent_state_2)

    def test_adding_agent(self):
        agent_state = AgentState(1, Vector2(100, 200), Vector2(0, 5), 10)
        self.pe.add_agent(agent_state)
        self.pe.step(1)
        assert(len(self.pe.space.bodies) == 1)
        assert(agent_state.position.x == 100)
        assert(agent_state.position.y == 205)

    def test_adding_projectile(self):
        projectile_state = ProjectileState(1, Vector2(100, 200), Vector2(10, 20), 1)
        self.pe.add_projectile(projectile_state)
        self.pe.step(1)
        assert(len(self.pe.space.bodies) == 1)
        assert(projectile_state.position.x == 110)
        assert(projectile_state.position.y == 220)

    def test_adding_obstacle(self):
        agent_state = AgentState(1, Vector2(0, 100), Vector2(100, 0), 30)
        obstacle = Obstacle(2, Vector2(100, 70), 30, 30)
        self.pe.add_agent(agent_state)
        self.pe.add_obstacle(obstacle)
        self.pe.step(2)
        assert(self.callback.called)
        assert(len(self.pe.space.bodies) == 2)

    def test_agent_id_exception(self):
        agent_state = AgentState(1, Vector2(100, 200), Vector2(0, 100), 10)
        self.pe.add_agent(agent_state)
        agent_state_2 = AgentState(1, Vector2(100, 200), Vector2(0, 100), 10)
        with self.assertRaises(ValueError):
            self.pe.add_agent(agent_state_2)

    def test_projectile_id_exception(self):
        projectile_state = ProjectileState(1, Vector2(100, 200), Vector2(10, 20), 1)
        self.pe.add_agent(projectile_state)
        projectile_state_2 = ProjectileState(1, Vector2(100, 200), Vector2(10, 20), 1)
        with self.assertRaises(ValueError):
            self.pe.add_agent(projectile_state_2)

    def test_removing_object(self):
        agent_state = AgentState(1, Vector2(100, 200), Vector2(0, 100), 10)
        self.pe.add_agent(agent_state)
        self.pe.remove_object(agent_state.id)
        self.pe.step(1)
        assert(len(self.pe.space.bodies) == 0)
        assert(agent_state.position.x == 100)
        assert(agent_state.position.y == 200)

    def test_upper_boundary(self):
        agent_state = AgentState(1, Vector2(50, PhysicsEngine.SPACE_HEIGHT), Vector2(0, 1), 10)
        self.pe.add_agent(agent_state)
        self.pe.step(1)
        assert(self.callback.called)

    def test_right_boundary(self):
        agent_state = AgentState(1, Vector2(PhysicsEngine.SPACE_WIDTH, 50), Vector2(0, 1), 10)
        self.pe.add_agent(agent_state)
        self.pe.step(1)
        assert(self.callback.called)

    def test_left_boundary(self):
        agent_state = AgentState(1, Vector2(0, 50), Vector2(0, 1), 10)
        self.pe.add_agent(agent_state)
        self.pe.step(1)
        assert(self.callback.called)

    def test_lower_boundary(self):
        agent_state = AgentState(1, Vector2(50, 0), Vector2(0, 1), 10)
        self.pe.add_agent(agent_state)
        self.pe.step(1)
        assert(self.callback.called)

if __name__ == '__main__':
    unittest.main()