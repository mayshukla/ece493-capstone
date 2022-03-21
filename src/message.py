import json

class Message():
    """Base class for messages to be passed between the server and client as JSON.
    """

    ## Declare message types here and also in message.js.
    ##   Explain what the message is for.
    ##   Also declare what will be contained in the data field.

    # Send message to print for debugging purposes.
    # data: string to that should be printed to terminal/console
    DEBUG = "debug"

    # Tell client that game is starting. (Matchmaking is over)
    # data: None
    START_GAME = "start_game"

    # Tell client that the simulation is starting. (Code submission is done)
    # data: None
    START_SIMULATION = "start_simulation"

    # Used by client to send player's inputted python code.
    # data: {
    #     code: code as string
    #     class_name: name of the Agent subclass created by the player
    # }
    PLAYER_CODE = "player_code"

    # Used by server to send python errors to client when player code causes
    # errors.
    # data: error message as string
    PYTHON_ERROR = "python_error"

    def __init__(self, _type, data):
        """Constructor

        Arguments:
            type: One of the message type strings declared above (e.g. Message.Debug)
            data: Any type that has a __str__() method (this will be used to jsonify).
                The type of data may be different for different message types.
        """
        self.type = _type
        self.data = data

    def to_json(self):
        """Returns json string representation.
        """
        json_dict = {
            "type": self.type,
            "data": self.data.__str__() if self.data is not None else None
        }

        return json.dumps(json_dict)

    def from_json(json_str):
        """Converts json string to a Message instance.
        """
        json_dict = json.loads(json_str)
        return Message(
            json_dict["type"],
            json_dict["data"]
        )