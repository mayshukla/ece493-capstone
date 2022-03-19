import initPixi from "./gameSetup.js";

/**
 * Deals with UI and rendering.
 */
export default class Renderer {
    #server;
    #codeArea;
    #classNameArea;
    #submitButton;
    #pythonErrorsArea;
    #queueScreen;
    #codeInputScreen;

    constructor(clientToServerConnection) {
        this.#server = clientToServerConnection;

        this.#codeArea = document.getElementById("codeArea");
        this.#classNameArea = document.getElementById("classNameArea");
        this.#submitButton = document.getElementById("submitButton")
        this.#submitButton.onclick = () => { this.#sendCodeToServer() };

        this.#pythonErrorsArea = document.getElementById("pythonErrorsArea");
        this.#server.onPythonError = (error) => { this.#onPythonError(error); };

        this.#server.onStartGame = () => { this.#onStartGame(); };
        this.#server.onStartSimulation = () => { this.#onStartSimulation(); };

        this.#queueScreen = document.getElementById("queueScreen");
        this.#codeInputScreen = document.getElementById("codeInputScreen");
    }

    #sendCodeToServer() {
        let code = this.#codeArea.value;
        let className = this.#classNameArea.value;
        this.#server.sendCode(code, className);
    }

    #onPythonError(error) {
        this.#pythonErrorsArea.textContent = error;
    }

    #onStartGame() {
        this.#queueScreen.classList.add("hidden");
        this.#codeInputScreen.classList.remove("hidden");
        this.#pythonErrorsArea.classList.remove("hidden");
    }

    #onStartSimulation() {
        this.#codeInputScreen.classList.add("hidden");

        // Initialize the Pixi canvas
        initPixi();
    }
}