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
        this.#websocket.onmessage = this.#onmessage;
    }

    #onmessage(message_str) {
        let message = Message.fromJson(message_str.data);

        // TODO handle all message types
        switch (message.type) {
            case Message.DEBUG:
                console.log(message.data);
                break;
            default:
                console.error("ERROR: unhandled message type. Message: ${message}");
        }
    }

    sendCode(code) {
        let message = new Message(
            Message.PLAYER_CODE,
            code
        );
        this.sendMessage(message);
    }

    sendMessage(message) {
        this.#websocket.send(message.toJson());
    }
}