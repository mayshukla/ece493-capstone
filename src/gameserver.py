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
        client.send_debug_message("Entered matchmaking queue.")

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
            client.send_start_game_message()

        # TODO create Game instance