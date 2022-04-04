/**
 * JS implementation of Message class.
 * See message.py
 * Specifies the types of messages that may be passed between the server and client.
 * 
 * This module is part of the implementation of the following requirements:
 * FR1 - UI.InputCode
 * FR2 - UI.RunGame
 * FR4 - UI.ConsistentState
 * FR5 - UI.ResultsScreen
 */
export default class Message {
    static DEBUG = "debug";
    static START_GAME = "start_game";
    static PLAYER_CODE = "player_code";
    static PYTHON_ERROR = "python_error";
    static START_SIMULATION = "start_simulation";
    static PROJECTILE_STATES = "projectile_states";
    static DESTROY = "destroy";
    static AGENT_STATES = "agent_states";
    static RESULTS = "results";

    constructor(type, data) {
        this.type = type;
        this.data = data;
    }

    toJson() {
        let jsonObj = {
            "type": this.type,
            "data": this.data
        };
        return JSON.stringify(jsonObj);
    }

    static fromJson(jsonString) {
        let jsonObj = JSON.parse(jsonString);
        return new Message(
            jsonObj.type,
            jsonObj.data
        );
    }
}