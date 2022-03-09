import argparse
import tornado.ioloop
import tornado.web


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help="Port for server to listen on.")
    args = parser.parse_args()
    port = args.port

    application = tornado.web.Application([
        (
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