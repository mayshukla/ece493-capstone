/**
 * JS implementation of Message class.
 * See message.py
 */
export default class Message {
    static DEBUG = "debug";
    static START_GAME = "debug";
    static PLAYER_CODE = "player_code";
    static PYTHON_ERROR = "python_error";
    static START_SIMULATION = "start_simulation";

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