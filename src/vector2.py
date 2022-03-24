class Vector2():
    """A 2 dimensional vector class. Wrapper around x and y coordinates."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Allows Vector2 instances to be compared using =="""
        return self.x == other.x and self.y == other.y
