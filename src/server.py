import argparse
import tornado.ioloop
import tornado.web
import tornado.websocket

from gameserver import GameServer
from message import Message
from agent_state import AgentState
from vector2 import Vector2


class ServerToClientConnection(tornado.websocket.WebSocketHandler):
    """Represents a connection from the server to a single client.

    Abstracts away websocket details.
    """
    def initialize(self, game_server):
        # Get reference to game server
        self.game_server = game_server

    def open(self, **kwargs):
        print("New ServerToClientConnection")

        self.write_message("hello from server")

        # Place self in queue
        self.game_server.enqueue(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("ServerToClientConnection closed")

    def send_agent_states(self, agent_states):
        message = Message(Message.AGENT_STATES, agent_states)
        self.write_message(message.to_json_array())

    def send_projectile_states(self, projectile_states):
        message = Message(Message.PROJECTILE_STATES, projectile_states)
        self.write_message(message.to_json_array())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Port for server to listen on.")
    args = parser.parse_args()
    port = args.port

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
            {"path": "frontend", "default_filename": "index.html"},
        ),
    ])
    application.listen(port)
    print(f"Server running on port {port}")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()