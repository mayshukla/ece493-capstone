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
    #resultsScreen;
    #declareWinnerArea;
    #individualResultsArea;
    #declareErrorArea;

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
        this.#server.onReceiveResults = (winner, tie, player_results, error) => { this.#onReceiveResults(winner, tie, player_results, error); };

        this.#queueScreen = document.getElementById("queueScreen");
        this.#codeInputScreen = document.getElementById("codeInputScreen");

        this.#resultsScreen = document.getElementById("resultsScreen");
        this.#declareWinnerArea = document.getElementById("declareWinnerArea");
        this.#individualResultsArea = document.getElementById("individualResultsArea");
        this.#declareErrorArea = document.getElementById("declareErrorArea");
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

    #onReceiveResults(winner, tie, player_results, error) {
        console.log("showing results!");
        document.getElementsByTagName("canvas")[0].classList.add("hidden");
        this.#resultsScreen.classList.remove("hidden");
        if (error) {
            this.#declareErrorArea.innerHTML = "Game ended due to error in player code."
        }
        if (tie) {
            this.#declareWinnerArea.innerHTML = "It's a Tie!";
        }
        else if (winner) {
            this.#declareWinnerArea.innerHTML = "You Win, Congratulations!";
        }
        else {
            this.#declareWinnerArea.innerHTML = "You Lost, Better Luck Next Time!";
        }
        var results_text = ""
        player_results.forEach(function(result) {
            results_text += result["class_name"];
            if (result["survival_time"] == null) {
                results_text += " survived the entire game!" + "<br/>";
            }
            else {
                results_text += " survived for " + result["survival_time"].toString() + " seconds<br/>";
            }
        });
        this.#individualResultsArea.innerHTML = results_text;
    }
}