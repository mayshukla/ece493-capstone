from agent_state import AgentState

class Agent:
    """Base class for an Agent that should be extended by player code.
    """
    def __init__(self, agent_state):
        self.agent_state = agent_state