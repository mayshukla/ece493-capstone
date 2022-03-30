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

    # Send client the current state of each agent
    # data: a list of AgentStates
    AGENT_STATES = "agent_states"

    # Send client the current state of each agent
    # data: a list of ProjectileStates
    PROJECTILE_STATES = "projectile_states"

    # Send client the id of an object that was destroyed
    # data: {
    #     id: id of destroyed object
    #     type: type of destroyed object. Possible values: "agent", "projectile"
    # }
    DESTROY = "destroy"

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

    # Tells the client that the game has ended and provides the results to display
    # data: {
    #     winner: bool indicating whether the client receiving this message won
    #     tie: bool indicating whether the game ended in a tie
    #     players: {
    #        class_name: name of the class submitted by the player
    #        survival_time: float survival time in seconds or None if the player survived the entire game
    #     }
    # }
    RESULTS = "results"

    def __init__(self, _type, data):
        """Constructor

        Arguments:
            type: One of the message type strings declared above (e.g. Message.Debug)
            data: Any type that has a __str__() method (this will be used to jsonify).
                The type of data may be different for different message types. May also be a list
                of any type that implements the to_json_dict() method.
        """
        self.type = _type
        self.data = data

    def to_json(self):
        """Returns json string representation.
        """
        if isinstance(self.data, list):
            # if data is a list convert it to a json array
            data = [object.to_json_dict() for object in self.data]
        elif isinstance(self.data, dict):
            # a dict will be converted by json.dumps. don't convert it to a
            # string.
            data = self.data
        elif self.data is not None:
            # otherwise if data is not none convert it to a string
            data = self.data.__str__()
        else:
            data = None
        json_dict = {
            "type": self.type,
            "data": data
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