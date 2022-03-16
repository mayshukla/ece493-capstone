from collections import deque

class GameServer():
    """Manages client queue and starts and ends games.
    """
    def __init__(self):
        self.queue = deque()

    def enqueue(self, client):
        """Places a client in the queue.
        """
        self.queue.appendleft(client)
        client.write_message("Entered matchmaking queue.")

        if len(self.queue) >= 2:
            clients = []
            clients.append(self.queue.pop())
            clients.append(self.queue.pop())
            self.start_game(clients)

    def remove_from_queue(self, client):
        """Removes a client from the queue.
        """
        self.queue.remove(client)

    def start_game(self, clients):
        """Creates and starts a game with the given list of clients.
        """
        print("Starting a new game")
        for client in clients:
            client.write_message("Found match. Starting game...")

        # TODO create Game instance