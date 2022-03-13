import unittest
from unittest.mock import MagicMock

from src.message import *
from src.physics_engine import *

class TestPhysicsEngine(unittest.TestCase):

    def setUp(self):
        self.pe = PhysicsEngine()

    def test_collision_callback(self):
        callback = MagicMock()
        self.pe.addOnCollisionCallback(callback)
        circle1 = self.pe.create_circle((100, 200), 30)
        circle2 = self.pe.create_circle((300, 200), 30)
        circle1.body.velocity = (5, 0)
        self.pe.space.step(40)
        assert(callback.called)

if __name__ == '__main__':
    unittest.main()