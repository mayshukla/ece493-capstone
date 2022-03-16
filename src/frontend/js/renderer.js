/**
 * Deals with UI and rendering.
 */
export default class Renderer {
    #server;
    #codeArea;
    #submitButton;

    constructor(clientToServerConnection) {
        this.#server = clientToServerConnection;

        this.#codeArea = document.getElementById("codeArea");
        this.#submitButton = document.getElementById("submitButton")
        this.#submitButton.onclick = () => { this.#sendCodeToServer() };
    }

    #sendCodeToServer() {
        let code = this.#codeArea.value;
        this.#server.sendCode(code);
    }
}