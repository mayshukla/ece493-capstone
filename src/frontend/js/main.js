/*
* This module initializes the client-server connection and the game renderer, which are related to 
* the following functional requirements:
* 
* FR2 - UI.RunGame
* FR3 - UI.RenderGame
* FR4 - UI.ConsistentState
* FR5 - UI.ResultsScreen
*/

import ClientToServerConnection from "./clienttoserverconnection.js";
import Renderer from "./renderer.js";

function main() {
    const conn = new ClientToServerConnection();
    const renderer = new Renderer(conn);
}

window.onload = main