/*
 * Initializes the game visuals and updates the rendering based on server messages.
 *
 * This module satisfies the following functional requirements:
 * FR3 - UI.RenderGame
 * FR4 - UI.ConsistentState
 */

//Aliases
const Application = PIXI.Application,
  loader = PIXI.Loader.shared,
  resources = PIXI.Loader.shared.resources,
  Sprite = PIXI.Sprite,
  TextureCache = PIXI.utils.TextureCache,
  Rectangle = PIXI.Rectangle,
  AnimatedSprite = PIXI.AnimatedSprite,
  Container = PIXI.Container,
  ParticleContainer = PIXI.ParticleContainer,
  Texture = PIXI.Texture,
  Text = PIXI.Text;

const PI = 3.14,
  PLAYABLE_AREA_X_MIN = 65,
  PLAYABLE_AREA_X_MAX = 1024 - PLAYABLE_AREA_X_MIN,
  PLAYABLE_AREA_Y_MIN = 25,
  PLAYABLE_AREA_Y_MAX = 700 - PLAYABLE_AREA_Y_MIN,
  AGENT_GUN_X_PX = 244,
  AGENT_GUN_Y_PX = 162,
  AGENT_GUN_X_NORM = 0.95686,
  AGENT_GUN_Y_NORM = 0.75349,
  TEXT_NAME_STYLE = {
    // fill: "red",
    fill: "#6dc2ca",
    fontFamily: "Tahoma",
    // fontFamily: "Arial",
    fontSize: 75,
    letterSpacing: 1,
    fontWeight: 600,
    lineJoin: "bevel",
  };

let app,
  agentSheet,
  id,
  gameState,
  obstacleSheet,
  obstacleSSheet,
  projectileSpeed;

export let agents = [];
export let projectileMap = new Map();
export let agent0NameSet = false;
export let agent1NameSet = false;

export default function initPixi() {
  //Create a Pixi Application
  app = new Application({
    width: 1024, // default: 800
    height: 700, // default: 600
    antialias: true, // default: false
    transparent: false, // default: false
    resolution: 1, // default: 1
  });

  //Add the canvas that Pixi automatically created for you to the HTML document
  document.body.appendChild(app.view);
  app.renderer.autoDensity = true;

  //load an image and run the `setup` function when it's done
  loader
    .add("../assets/dungeon.json")
    .add("../assets/agentsheet.json")
    .add("../assets/agentsheet.png")
    .add("../assets/obstacleboxes.json")
    .add("../assets/obstacleboxes.png")
    .add("../assets/bulletSprite.png")
    .load(setup);
}

//This `setup` function will run when the image has loaded
function setup() {
  //#region SpriteAssetsCreation

  id = resources["../assets/dungeon.json"].textures;
  agentSheet = resources["../assets/agentsheet.json"];
  obstacleSSheet = new PIXI.BaseTexture.from("../assets/obstacleboxes.png");

  let obstacles = createObstacles(obstacleSSheet);
  agents = createAgents(agentSheet);

  projectileSpeed = 5;

  let background = new Sprite(id["dungeon.png"]);
  background.scale.set(2, 1.367);
  //   agent size and obstacle size are 50 px

  //#endregion

  app.stage.addChild(background);
  app.stage.addChild(obstacles);
  app.stage.addChild(agents[0], agents[1]);

  //   Start game loop
  // app.ticker.add((delta) => gameLoop(delta));

  //   set the game state to play
  gameState = play;
}

function changeAgentAnimation(agent, animation) {
  switch (animation) {
    case "survivor-shield_handgun":
      agent.textures =
        agentSheet.spritesheet.animations["survivor-shield_handgun"];
      break;

    case "survivor-move_handgun":
      agent.textures =
        agentSheet.spritesheet.animations["survivor-move_handgun"];
      agent.loop = true;
      agent.animationSpeed = 0.3;
      agent.play();
      break;

    case "survivor-idle_handgun":
      agent.textures =
        agentSheet.spritesheet.animations["survivor-idle_handgun"];
      agent.loop = true;
      agent.animationSpeed = 0.3;
      agent.play();
      break;

    default:
      break;
  }
}

function gameLoop(delta) {
  // this calls the play fxn 60 times per minute
  // gameState(delta);
}

function play(delta) {
  // if (agents[0].angle !== agents[0].targetAngle) {
  //   if (agents[0].angle < agents[0].targetAngle) {
  //     updateAgentAngle(agents[0], true);
  //   } else {
  //     updateAgentAngle(agents[0], false);
  //   }
  // }
  // if (agents[1].angle !== agents[1].targetAngle) {
  //   if (agents[1].angle < agents[1].targetAngle) {
  //     updateAgentAngle(agents[1], true);
  //   } else {
  //     updateAgentAngle(agents[1], false);
  //   }
  // }
  // if (
  //   agents[0].vx !== agents[0].targetVx ||
  //   agents[0].vy !== agents[0].targetVy
  // ) {
  //   updateAgentPosition(agents[0]);
  // }
  // if (
  //   agents[1].vx !== agents[1].targetVx ||
  //   agents[1].vy !== agents[1].targetVy
  // ) {
  //   updateAgentPosition(agents[1]);
  // }
}

function updateAgentAngle(agent, positiveRotation) {
  // For testing purposes this is disabled, but when client
  // starts receiving messages concerning agent movements
  // this will be enabled

  if (positiveRotation) {
    agent.angle += 2;
  } else {
    agent.angle -= 2;
  }
}

function updateAgentPosition(agent) {
  agent.vx = agent.targetVx;
  agent.vy = agent.targetVy;

  if (agent.vx === 0 && agent.vy === 0) {
    agent.Moving = false;
  } else {
    agent.Moving = true;
  }

  // console.log(agentMoving);

  //Apply the velocity values to the idle shooter's
  //position to make it move
  agent.x += vx;
  agent.y += vy;
}

function createSpriteFromSheet(path, x, y, width, height) {
  let texture = TextureCache[path];
  let textureRect = new Rectangle(x, y, width, height);
  texture.frame = textureRect;
  let sprite = new Sprite(texture);
  return sprite;
}

function createObstacles(obstacleSSheet) {
  let obstacles = new Container();
  let midObstacles = new Container();
  let leftObstacles = new Container();
  let rightObstacles = new Container();
  // server x - 45, server y - 32
  let init_x = PLAYABLE_AREA_X_MIN + 27 + 64;
  let init_y = 105;
  let ratio = 1.25;

  obstacleSheet = {};
  obstacleSheet["blueBox"] = [
    new Texture(obstacleSSheet, new Rectangle(1 * 32, 0, 32, 32)),
  ];
  obstacleSheet["greyBox1"] = [
    new Texture(obstacleSSheet, new Rectangle(3 * 32, 0, 32, 32)),
  ];
  obstacleSheet["pinkBox"] = [
    new Texture(obstacleSSheet, new Rectangle(5 * 32, 0, 32, 32)),
  ];

  let blueBox = new Sprite(obstacleSheet["blueBox"][0]);
  blueBox.scale.set(ratio);
  let blueBox2 = new Sprite(obstacleSheet["blueBox"][0]);
  blueBox2.scale.set(ratio);
  let blueBox3 = new Sprite(obstacleSheet["blueBox"][0]);
  blueBox3.scale.set(ratio);

  console.log(blueBox);

  blueBox.x = init_x;
  blueBox.y = init_y;
  blueBox2.x = blueBox.x;
  blueBox2.y = blueBox.y + 15 + 32;
  blueBox3.x = blueBox2.x;
  blueBox3.y = blueBox2.y + 15 + 32;
  leftObstacles.addChild(blueBox, blueBox2, blueBox3);

  init_x = PLAYABLE_AREA_X_MAX / 2 - 45;
  init_y = 350 - 30;

  let greyBox1 = new Sprite(obstacleSheet["greyBox1"][0]);
  greyBox1.scale.set(ratio);
  let greyBox2 = new Sprite(obstacleSheet["greyBox1"][0]);
  greyBox2.scale.set(ratio);
  let greyBox3 = new Sprite(obstacleSheet["greyBox1"][0]);
  greyBox3.scale.set(ratio);

  greyBox1.x = init_x;
  greyBox1.y = init_y;
  greyBox2.x = greyBox1.x + 20 + 32;
  greyBox2.y = greyBox1.y + 20 + 32;
  greyBox3.x = greyBox1.x - 20 - 32;
  greyBox3.y = greyBox1.y - 20 - 32;
  midObstacles.addChild(greyBox1, greyBox2, greyBox3);

  init_x = PLAYABLE_AREA_X_MAX - 69 - 96;
  init_y = 570 - 10;

  let pinkBox = new Sprite(obstacleSheet["pinkBox"][0]);
  pinkBox.scale.set(ratio);
  let pinkBox2 = new Sprite(obstacleSheet["pinkBox"][0]);
  pinkBox2.scale.set(ratio);
  let pinkBox3 = new Sprite(obstacleSheet["pinkBox"][0]);
  pinkBox3.scale.set(ratio);

  pinkBox.x = init_x;
  pinkBox.y = init_y;
  pinkBox2.x = pinkBox.x;
  pinkBox2.y = pinkBox.y - 15 - 32;
  pinkBox3.x = pinkBox2.x;
  pinkBox3.y = pinkBox2.y - 15 - 32;
  rightObstacles.addChild(pinkBox, pinkBox2, pinkBox3);

  // console.log(blueBox.x, blueBox.y);
  // console.log(blueBox2.x, blueBox2.y);
  // console.log(blueBox3.x, blueBox3.y);
  // console.log(blueBox4.x, blueBox4.y);
  // console.log(blueBox5.x, blueBox5.y);
  // console.log(greyBox1.x, greyBox1.y);
  // console.log(greyBox2.x, greyBox2.y);
  // console.log(greyBox3.x, greyBox3.y);
  // console.log(pinkBox.x, pinkBox.y);
  // console.log(pinkBox2.x, pinkBox2.y);
  // console.log(pinkBox3.x, pinkBox3.y);
  // console.log(pinkBox4.x, pinkBox4.y);
  // console.log(pinkBox5.x, pinkBox5.y);

  obstacles.addChild(leftObstacles, midObstacles, rightObstacles);

  return obstacles;
}

function createAgents(agentSheet) {
  let agents = [];

  // create an animated sprite from the json sheet in assets
  let agent0 = new AnimatedSprite(
    agentSheet.spritesheet.animations["survivor-idle_handgun"]
  );
  let agent1 = new AnimatedSprite(
    agentSheet.spritesheet.animations["survivor-idle_handgun"]
  );

  agents.push(agent0, agent1);

  // set speed, start playback and add it to the stage
  agent0.animationSpeed = 0.3;
  agent0.play();
  agent0.x = PLAYABLE_AREA_X_MIN + 65;
  agent0.y = 350;
  agent0.scale.set(0.197628458, 0.23148148);
  agent0.vx = 0;
  agent0.vy = 0;
  agent0.angle = 0;
  agent0["id"] = 0;
  agent0["ShieldEquipped"] = false;
  agent0.anchor.set(0.95652, 0.75);
  agent0.health = 100;
  let agentName = new Text("agent0", TEXT_NAME_STYLE);
  agentName.x = -230;
  agentName.y = -250;
  let agentHP = new Text("HP: " + agent0.health, TEXT_NAME_STYLE);
  agentHP.x = -230;
  agentHP.y = 50;
  agent0.addChild(agentName);
  agent0.addChild(agentHP);
  // console.log(agent0.getChildAt(0).getLocalBounds());

  agent1.animationSpeed = 0.3;
  agent1.play();
  agent1.x = PLAYABLE_AREA_X_MAX - 65;
  agent1.y = 350;
  agent1.scale.set(0.197628458, 0.23148148);
  agent1.vx = 0;
  agent1.vy = 0;
  agent1.angle = 180;
  agent1["id"] = 1;
  agent1["ShieldEquipped"] = false;
  agent1.anchor.set(0.95652, 0.75);
  agent1.health = 100;

  console.log(agents);

  return agents;
}

export function destroyAgent(agentId) {
  let agent = findAgent(agentId);
  agent.visible = false;
  console.log("app before", app);
  app.stage.removeChild(agent);
  console.log("app after", app);
}

export function setAgentName(agentId, agentName) {
  let agent = findAgent(agentId);

  agent.addChild(
    new Text(agentName, {
      fontFamily: "Arial",
      fontSize: 24,
      fill: 0xff1010,
      align: "center",
    })
  );
}


export function createProjectile(projId, agentId, angle, x, y) {
  let agent = findAgent(agentId);
  animateAttack(agent);

  var projectile = createSpriteFromSheet(
    "../assets/bulletSprite.png",
    0,
    0,
    257,
    76
  );
  projectile.width = 10;
  projectile.height = 5;
  projectile.anchor.set(0.5, 0.5);
  projectile.position.x = x;
  projectile.position.y = y;
  projectile.angle = angle;

  projectileMap.set(projId, projectile);
  console.log(projectileMap);
  app.stage.addChild(projectile);
}

export function updateProjectilePosition(projId, x, y) {
  let projectile = projectileMap.get(projId);
  projectile.x = x;
  projectile.y = y;
}

export function destroyProjectile(projId) {
  let projectile = projectileMap.get(projId);
  projectile.visible = false;
  app.stage.removeChild(projectile);
}

export function setAgentPosition(agent, x, y) {
  agent.x = x;
  agent.y = y;
}

export function setAgentDirection(agent, angle) {
  agent.angle = angle;
}

export function setAgentHealth(agent, health) {
  if (agent.health !== health) {
    // Damage taken
    animateDamage(agent);
  }
  agent.health = health;
}

export function toggleAgentShield(agent, shieldEnabled) {
  agent.stop();
  if (shieldEnabled) {
    agent.textures =
      agentSheet.spritesheet.animations["survivor-shield_handgun"];
  } else {
    agent.textures = agentSheet.spritesheet.animations["survivor-idle_handgun"];
  }
  agent.ShieldEquipped = !agent.ShieldEquipped;
  agent.loop = false;
  agent.animationSpeed = 0.5;
  agent.play();
}

function animateDamage(agent) {
  colorTint(agent, 0xFF0000);
}

function animateAttack(agent) {
  colorTint(agent, 0x00FF00);
}

function colorTint(agent, color) {
  let filter = new PIXI.filters.ColorMatrixFilter();
  filter.tint(color, true);
  filter.contrast(1, true);
  agent.filters = [filter];

  setTimeout(() => { agent.filters = [] }, 200);
}

function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function findAgent(agentId) {
  var agent = agents.find((obj) => {
    console.log(obj.id);
    console.log(agentId);
    return obj.id === agentId;
  });

  return agent;
}
