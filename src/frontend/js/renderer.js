/**
 * Deals with UI and rendering.
 */
export default class Renderer {
    #server;
    #codeArea;
    #classNameArea;
    #submitButton;
    #pythonErrorsArea;

    constructor(clientToServerConnection) {
        this.#server = clientToServerConnection;

        this.#codeArea = document.getElementById("codeArea");
        this.#classNameArea = document.getElementById("classNameArea");
        this.#submitButton = document.getElementById("submitButton")
        this.#submitButton.onclick = () => { this.#sendCodeToServer() };

        this.#pythonErrorsArea = document.getElementById("pythonErrorsArea");
        this.#server.onPythonError = (error) => { this.#onPythonError(error); };
    }

    #sendCodeToServer() {
        let code = this.#codeArea.value;
        let className = this.#classNameArea.value;
        this.#server.sendCode(code, className);
    }

    #onPythonError(error) {
        this.#pythonErrorsArea.textContent = error;
    }
}