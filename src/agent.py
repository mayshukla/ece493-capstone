from src.agent_state import AgentState
from src.vector2 import Vector2

class Agent:
    """Base class for an Agent that should be extended by player code.
    """
    def __init__(self, id):
        self.agent_state = AgentState(
            id,
            Vector2(0, 0),
            Vector2(0, 0),
            100
        )