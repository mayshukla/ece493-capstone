import ClientToServerConnection from "./clienttoserverconnection.js";
import Renderer from "./renderer.js";

function main() {
    const conn = new ClientToServerConnection();
    const renderer = new Renderer(conn);
}

window.onload = main