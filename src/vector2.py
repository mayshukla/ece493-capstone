import math

class Vector2():
    """A 2 dimensional vector class. Wrapper around x and y coordinates."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Allows Vector2 instances to be compared using =="""
        return self.x == other.x and self.y == other.y

    def get_angle(self):
        """returns the angle of the vector in degrees"""
        # atan2 handles cases where x is 0
        return math.degrees(math.atan2(self.y, self.x))

    def get_magnitude(self):
        """returns the magnitude of the vector"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def clone(self):
        """Returns a new Vector2 instance with the same x and y values."""
        return Vector2(self.x, self.y)

    @classmethod
    def from_angle_magnitude(vector2, angle, magnitude):
        """returns a vector object
        
        Arguments: 
        angle: the angle of the vector in degrees
        magnitude: the magnitude of the vector"""
      # create an object for the class to return
        y = math.sin(math.radians(angle)) * magnitude
        x = math.cos(math.radians(angle)) * magnitude
        return vector2(x, y)
