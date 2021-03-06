import Message from "./message.js";
import {
  agents,
  agent0NameSet,
  agent1NameSet,
  setAgentName,
  setAgentPosition,
  setAgentDirection,
  setAgentHealth,
  toggleAgentShield,
  projectileMap,
  createProjectile,
  updateProjectilePosition,
  updateAgentTextPosition,
  destroyProjectile,
  destroyAgent,
} from "./gameSetup.js";

/*
 * Handles server-client communication.
 *
 * This module is part of the following functional requirments:
 * FR2 - UI.RunGame
 * FR4 - UI.ConsistentState
 * FR5 - UI.ResultsScreen
 *
 */

/**
 * Represents connection from client to server.
 * Abstracts away websocket details.
 */
export default class ClientToServerConnection {
  #websocket;

  constructor() {
    const server_url =
      "ws://" +
      window.location.hostname +
      ":" +
      window.location.port +
      "/websocket";
    this.#websocket = new WebSocket(server_url);
    this.#websocket.onmessage = (msg) => {
      this.#onmessage(msg);
    };
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
      case Message.DESTROY:
        console.log(message);
        this.onReceiveDestroy(message.data.id, message.data.type);
        break;
      case Message.RESULTS:
        console.log(message.data);
        this.onReceiveResults(
          message.data["winner"],
          message.data["tie"],
          message.data["players"],
          message.data["error"]
        );
        break;
      default:
        console.error("ERROR: unhandled message type. Message:", message);
    }
  }

  sendCode(code, className) {
    let message = new Message(Message.PLAYER_CODE, {
      code: code,
      class_name: className,
    });
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
    console.log(agents);
    for (var agent_state of agent_states) {
      console.log(agent_state);
      //console.log(agent_state.position)
      //console.log(agent_state.position.x)
      var agent = agents.find((obj) => {
        console.log(obj.id);
        console.log(agent_state.id);
        return obj.id === agent_state.id;
      });
      console.log(agent);
      if (typeof agent === "undefined") {
        // create agent
        return false;
      } else {
        if (!agent0NameSet || !agent1NameSet) {
          setAgentName(agent_state.id, agent_state.name);
        }
        setAgentPosition(agent, agent_state.position.x, agent_state.position.y);
        setAgentDirection(agent, agent_state.angle);
        setAgentHealth(agent, agent_state.health);
        updateAgentTextPosition(
          agent,
          agent_state.position.x,
          agent_state.position.y
        );
        if (agent_state.shieldEnabled && !agent.ShieldEquipped) {
          toggleAgentShield(agent, agent_state.shieldEnabled);
        }
        if (!agent_state.shieldEnabled && agent.ShieldEquipped) {
          toggleAgentShield(agent, agent_state.shieldEnabled);
        }
      }
    }
  }

  onReceiveProjectileStates(projectile_states) {
    console.log(projectile_states);
    for (var projectile_state of projectile_states) {
      console.log(projectile_state);
      if (projectileMap.get(projectile_state.id) === undefined) {
        createProjectile(
          projectile_state.id,
          projectile_state.attackerId,
          projectile_state.angle,
          projectile_state.position.x,
          projectile_state.position.y
        );
      } else {
        updateProjectilePosition(
          projectile_state.id,
          projectile_state.position.x,
          projectile_state.position.y
        );
      }
    }
  }

  onReceiveDestroy(id, type) {
    console.log(`DESTROY id: ${id}, type: ${type}`);
    if (type === "projectile") {
      destroyProjectile(id);
    } else if (type === "agent") {
      destroyAgent(id);
    }
  }

  onReceiveResults(winner, tie, player_results, error) {
    console.log(player_results);
  }
}
