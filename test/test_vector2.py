import unittest
from unittest.mock import MagicMock

from src.vector2 import *
import math

class TestPhysicsEngine(unittest.TestCase):

    def test_vector_to_angle_magnitude(self):
        vector = Vector2(1, 1)
        assert(vector.x == 1)
        assert(vector.y == 1)
        assert(vector.get_angle() == 45)
        assert(vector.get_magnitude() == math.sqrt(2))
    
    def test_angle_magnitude_to_vector(self):
        vector_a = Vector2(5, 10)
        angle = vector_a.get_angle()
        magnitude = vector_a.get_magnitude()
        vector_b = Vector2.from_angle_magnitude(angle, magnitude)
        assert(math.isclose(vector_b.x, vector_a.x))
        assert(math.isclose(vector_b.y, vector_a.y))

if __name__ == '__main__':
    unittest.main()