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

    #onmessage(message) {
        console.log(message.data);
    }

    sendCode(code) {
        let msg = new Message(
            Message.PLAYER_CODE,
            code
        );
        this.sendMessage(msg);
    }

    sendMessage(msg) {
        this.#websocket.send(msg.toJson());
    }
}