import unittest

from src.message import *


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


if __name__ == '__main__':
    unittest.main()