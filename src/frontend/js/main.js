import ClientToServerConnection from "./clienttoserverconnection.js";

function main() {
    console.log("hello from main.js");

    const conn = new ClientToServerConnection();
}

window.onload = main