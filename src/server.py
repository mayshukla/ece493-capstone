"""
Handles starting the game server and server-client communication.

This module is part of the implementation of the following requirement:
FR4 - UI.ConsistentState
"""

import argparse
import mimetypes
from traceback import format_exception
import tornado.ioloop
import tornado.web
import tornado.websocket

from src.gameserver import GameServer
from src.message import Message


class ServerToClientConnection(tornado.websocket.WebSocketHandler):
    """Represents a connection from the server to a single client.

    Abstracts away websocket details.
    """
    def initialize(self, game_server):
        # Get reference to game server
        self.game_server = game_server

        # Callback which can be set by other classes
        self.on_receive_player_code = None

    def open(self, **kwargs):
        print("New ServerToClientConnection")

        self.send_debug_message("hello from server")

        # Place self in queue
        self.game_server.enqueue(self)

    def on_message(self, message_str):
        message = Message.from_json(message_str)
        message_type = message.type

        if message_type == Message.DEBUG:
            print(message.data)
        if message_type == Message.PLAYER_CODE:
            self.handle_player_code_message(message)
        else:
            print(f"ERROR: unhandled message type: {message.type}")

    def on_close(self):
        print("ServerToClientConnection closed")
        self.game_server.remove_from_queue(self)

    def send_message(self, message):
        """Send a Message object.
        """
        self.write_message(message.to_json())

    def send_debug_message(self, message_contents):
        message = Message(
            Message.DEBUG,
            message_contents
        )
        self.send_message(message)

    def send_start_game_message(self):
        message = Message(
            Message.START_GAME,
            None
        )
        self.send_message(message)

    def send_start_simulation_message(self):
        message = Message(
            Message.START_SIMULATION,
            None
        )
        self.send_message(message)

    def send_python_error(self, e_type, e_value, e_traceback):
        error_str = format_exception(e_type, e_value, e_traceback)
        error_str = "".join(error_str)
        message = Message(
            Message.PYTHON_ERROR,
            error_str
        )
        self.send_message(message)

    def send_results(self, winner, tie, agents, error=False):
        message = Message(Message.RESULTS, {
            "winner": winner,
            "tie": tie,
            "error": error,
            "players": [
                {
                    "class_name": type(agents[0][1]).__name__,
                    "survival_time": agents[0][1].survival_time
                },
                {
                    "class_name": type(agents[1][1]).__name__,
                    "survival_time": agents[1][1].survival_time
                }
            ]
        })
        self.send_message(message)

    def handle_player_code_message(self, message):
        code = message.data["code"]
        class_name = message.data["class_name"]
        if self.on_receive_player_code is not None:
            self.on_receive_player_code(self, code, class_name)

    def send_agent_states(self, agent_states):
        message = Message(Message.AGENT_STATES, agent_states)
        self.write_message(message.to_json())

    def send_projectile_states(self, projectile_states):
        message = Message(Message.PROJECTILE_STATES, projectile_states)
        self.write_message(message.to_json())

    def send_destroy_message(self, object_id, object_type):
        message = Message(Message.DESTROY, {
            "id": object_id,
            "type": object_type
        })
        self.write_message(message.to_json())


def fix_mime_types():
    """Manually register mimetypes to fix some weird behaviour on windows.

    The mimetypes modules reades from the windows registry.
    Sometimes the registry contains entries that produce the wrong mimetype.
    If the mimetype of a .js file is wrong, the browser will refuse to run it.

    See: https://bugs.python.org/issue43975
    """
    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/html", ".html")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Port for server to listen on.")
    args = parser.parse_args()
    port = args.port

    fix_mime_types()

    game_server = GameServer()

    application = tornado.web.Application([
        (
            # Handle websocket connections at the url /websocket.
            # This will create a new instance of ServerToClientConnection for each client.
            r"/websocket",
            ServerToClientConnection,
            {"game_server": game_server},
        ),
        (
            # Handle http requests at the root url.
            # StaticFileHandler simply serves static files.
            r"/(.*)",
            tornado.web.StaticFileHandler,
            {"path": "src/frontend", "default_filename": "index.html"},
        ),
    ])
    application.listen(port)
    print(f"Server running on port {port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()