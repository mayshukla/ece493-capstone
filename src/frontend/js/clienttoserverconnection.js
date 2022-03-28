import Message from './message.js';
import {agents} from './gameSetup.js';

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
            case Message.START_GAME:
                this.onStartGame();
                break;
            case Message.START_SIMULATION:
                this.onStartSimulation();
                break;
            case Message.AGENT_STATES:
                this.onReceiveAgentStates(message.data);
                break;
            case Message.PROJECTILE_STATES:
                this.onReceiveProjectileStates(message.data);
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

    /**
     * Can be overwritten by another class.
     */
    onPythonError(error) {
        console.error(error);
    }

    /**
     * Can be overwritten by another class.
     */
    onStartGame(error) {
        console.log("START_GAME message received");
    }

    /**
     * Can be overwritten by another class.
     */
    onStartSimulation(error) {
        console.log("START_SIMULATION message received");
    }

    onReceiveAgentStates(agent_states) {
        console.log(agent_states);
        console.log(agents)
        for (var agent_state of agent_states) {
            console.log(agent_state)
            //console.log(agent_state.position)
            //console.log(agent_state.position.x)
            var agent = agents.find(obj => {
                console.log(obj.id);
                console.log(agent_state.id);
                return obj.id === agent_state.id
            })
            console.log(agent);
            if (typeof agent === 'undefined') {
                // create agent
                return false;
            }
            else {
                // setAgentPosition(agent, agent_state.position.x, agent_state.position.y);
            }
        }
    }

    onReceiveProjectileStates(projectile_states) {
        console.log(projectile_states);
    }
}
