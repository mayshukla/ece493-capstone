import ClientToServerConnection from "./clienttoserverconnection.js";
import Renderer from "./renderer.js";

function main() {
    console.log("hello from main.js");

    const conn = new ClientToServerConnection();
    const renderer = new Renderer(conn);
}

window.onload = main