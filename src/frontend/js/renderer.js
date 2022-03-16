/**
 * Deals with UI and rendering.
 */
export default class Renderer {
    #server;
    #codeArea;
    #classNameArea;
    #submitButton;

    constructor(clientToServerConnection) {
        this.#server = clientToServerConnection;

        this.#codeArea = document.getElementById("codeArea");
        this.#classNameArea = document.getElementById("classNameArea");
        this.#submitButton = document.getElementById("submitButton")
        this.#submitButton.onclick = () => { this.#sendCodeToServer() };
    }

    #sendCodeToServer() {
        let code = this.#codeArea.value;
        let className = this.#classNameArea.value;
        this.#server.sendCode(code, className);
    }
}