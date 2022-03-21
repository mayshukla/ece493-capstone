import unittest

from src.message import *
from src.agent_state import *
from src.vector2 import *
from src.projectile_state import *


class TestMessage(unittest.TestCase):

    def message_test_helper(self, msg):
        json_str = msg.to_json()
        new_msg = Message.from_json(json_str)

        self.assertEqual(msg.type, new_msg.type)
        self.assertEqual(msg.data, new_msg.data)

    def test_debug_message(self):
        msg = Message(Message.DEBUG, "some debug message")
        self.message_test_helper(msg)

    def test_start_game_message(self):
        msg = Message(Message.START_GAME, None)
        self.message_test_helper(msg)

    def test_agent_state_message(self):
        msg = Message(Message.AGENT_STATES, [AgentState(1, Vector2(100, 200), Vector2(0, 0), 10), AgentState(2, Vector2(300, 400), Vector2(10, 10), 20)])
        expected_json = json.dumps({
            "type": Message.AGENT_STATES,
            "data": [
                {"id": 1, "position": {"x": 100, "y": 200}, "velocity": {"x": 0, "y": 0}, "health": 10, "shieldEnabled": False},
                {"id": 2, "position": {"x": 300, "y": 400}, "velocity": {"x": 10, "y": 10}, "health": 20, "shieldEnabled": False}
            ]
        })
        self.assertEqual(msg.to_json(), expected_json)

    def test_projectile_state_message(self):
        msg = Message(Message.PROJECTILE_STATES, [ProjectileState(1, Vector2(100, 200), Vector2(0, 0), 3), ProjectileState(2, Vector2(300, 400), Vector2(10, 10), 4)])
        expected_json = json.dumps({
            "type": Message.PROJECTILE_STATES,
            "data": [
                {"id": 1, "position": {"x": 100, "y": 200}, "velocity": {"x": 0, "y": 0}, "attackerId": 3},
                {"id": 2, "position": {"x": 300, "y": 400}, "velocity": {"x": 10, "y": 10}, "attackerId": 4}
            ]
        })
        self.assertEqual(msg.to_json(), expected_json)


if __name__ == '__main__':
    unittest.main()