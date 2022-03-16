import Message from './message.js';

/**
 * Represents connection from client to server.
 * Abstracts away websocket details.
 */
export default class ClientToServerConnection {
    #websocket;

    constructor() {
        const server_url = "ws://" + window.location.hostname + ":" + window.location.port + "/websocket";
        this.#websocket = new WebSocket(server_url);
        this.#websocket.onmessage = (msg) => { this.#onmessage(msg) };
    }

    #onmessage(message_str) {
        let message = Message.fromJson(message_str.data);

        // TODO handle all message types
        switch (message.type) {
            case Message.DEBUG:
                console.log(message.data);
                break;
            case Message.PYTHON_ERROR:
                this.onPythonError(message.data);
                break;
            default:
                console.error("ERROR: unhandled message type. Message:", message);
        }
    }

    sendCode(code, className) {
        let message = new Message(
            Message.PLAYER_CODE,
            {
                "code": code,
                "class_name": className
            }
        );
        this.sendMessage(message);
    }

    sendMessage(message) {
        this.#websocket.send(message.toJson());
    }

    onPythonError(error) {
        console.error(error);
    }
}