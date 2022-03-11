import argparse
import tornado.ioloop
import tornado.web
import tornado.websocket


class ServerToClientConnection(tornado.websocket.WebSocketHandler):
    """Represents a connection from the server to a single client.

    Abstracts away websocket details.
    """
    def open(self):
        print("New ServerToClientConnection")
        self.write_message("hello from server")

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("ServerToClientConnection closed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Port for server to listen on.")
    args = parser.parse_args()
    port = args.port

    application = tornado.web.Application([
        (
            # Handle websocket connections at the url /websocket.
            # This will create a new instance of ServerToClientConnection for each client.
            r"/websocket",
            ServerToClientConnection,
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