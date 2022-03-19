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
  Texture = PIXI.Texture;

const PI = 3.14,
  PLAYABLE_AREA_X_MIN = 65,
  PLAYABLE_AREA_X_MAX = 1024 - PLAYABLE_AREA_X_MIN,
  PLAYABLE_AREA_Y_MIN = 25,
  PLAYABLE_AREA_Y_MAX = 700 - PLAYABLE_AREA_Y_MIN,
  AGENT_GUN_X_PX = 244,
  AGENT_GUN_Y_PX = 162,
  AGENT_GUN_X_NORM = 0.95686,
  AGENT_GUN_Y_NORM = 0.75349;

let app;

let agentSheet,
  id,
  agent,
  agentMoving = false,
  gameState,
  obstacleSheet,
  obstacleSSheet,
  projectileList,
  projectileSpeed;

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
    .add("../assets/sample.png")
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

  //Create the shooter sprite
  id = resources["../assets/dungeon.json"].textures;
  agentSheet = resources["../assets/agentsheet.json"];

  //#region Creating Obstacles
  let obstacles = new ParticleContainer(1500, {
    rotation: true,
    tint: true,
    vertices: true,
    uvs: true,
  });
  obstacleSSheet = new PIXI.BaseTexture.from("../assets/obstacleboxes.png");
  obstacleSheet = {};

  obstacleSheet["yellowBox"] = [
    new Texture(obstacleSSheet, new Rectangle(0 * 32, 0, 32, 32)),
  ];
  obstacleSheet["blueBox"] = [
    new Texture(obstacleSSheet, new Rectangle(1 * 32, 0, 32, 32)),
  ];
  obstacleSheet["orangeBox"] = [
    new Texture(obstacleSSheet, new Rectangle(2 * 32, 0, 32, 32)),
  ];
  obstacleSheet["greyBox1"] = [
    new Texture(obstacleSSheet, new Rectangle(3 * 32, 0, 32, 32)),
  ];
  obstacleSheet["greyBox2"] = [
    new Texture(obstacleSSheet, new Rectangle(4 * 32, 0, 32, 32)),
  ];
  obstacleSheet["pinkBox"] = [
    new Texture(obstacleSSheet, new Rectangle(5 * 32, 0, 32, 32)),
  ];

  let yellowBox = new Sprite(obstacleSheet["yellowBox"][0]);
  yellowBox.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  yellowBox.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(yellowBox);

  let blueBox = new Sprite(obstacleSheet["blueBox"][0]);
  blueBox.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  blueBox.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(blueBox);

  let orangeBox = new Sprite(obstacleSheet["orangeBox"][0]);
  orangeBox.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  orangeBox.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(orangeBox);

  let greyBox1 = new Sprite(obstacleSheet["greyBox1"][0]);
  greyBox1.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  greyBox1.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(greyBox1);

  let greyBox2 = new Sprite(obstacleSheet["greyBox2"][0]);
  greyBox2.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  greyBox2.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(greyBox2);

  let pinkBox = new Sprite(obstacleSheet["pinkBox"][0]);
  pinkBox.x = getRndInteger(PLAYABLE_AREA_X_MIN, PLAYABLE_AREA_X_MAX);
  pinkBox.y = getRndInteger(PLAYABLE_AREA_Y_MAX, PLAYABLE_AREA_Y_MIN);
  obstacles.addChild(pinkBox);

  //#endregion

  // create an animated sprite from the json sheet in assets
  agent = new AnimatedSprite(
    agentSheet.spritesheet.animations["survivor-idle_handgun"]
  );
  console.log(agent);

  // set speed, start playback and add it to the stage
  agent.animationSpeed = 0.3;
  agent.play();
  agent.x = 65;
  agent.y = 350;
  agent.scale.set(0.197628458, 0.23148148);
  agent.vx = 0;
  agent.vy = 0;
  agent.angle = 100;
  agent["vAngle"] = 0;
  agent.anchor.set(0.95652, 0.75);

  projectileList = [];
  projectileSpeed = 5;

  const background = new Sprite(id["dungeon.png"]);
  background.scale.set(2, 1.367);
  //   agent size and obstacle size are 50 px

  //#endregion

  app.stage.addChild(background);
  app.stage.addChild(obstacles);
  app.stage.addChild(agent);

  //   Start game loop
  app.ticker.add((delta) => gameLoop(delta));

  // start listening for key input to move shoooter
  moveShooter(agent);
  fireProjectile(agent);

  //   set the game state to play
  gameState = play;
}

function gameLoop(delta) {
  // this calls the play fxn 60 times per minute
  gameState(delta);
}

function play(delta) {
  updateAgentPosition(agent, agent.vx, agent.vy);
  updateProjectiles(projectileList, projectileSpeed);
  updateAgentAngle(agent, agent.vAngle);

  if (agentMoving) {
    if (!agent.playing) {
      agent.textures =
        agentSheet.spritesheet.animations["survivor-move_handgun"];
      agent.loop = true;
      agent.animationSpeed = 0.3;
      agent.play();
    }
  }

  if (!agentMoving) {
    if (!agent.playing) {
      agent.textures =
        agentSheet.spritesheet.animations["survivor-idle_handgun"];
      agent.loop = true;
      agent.animationSpeed = 0.3;
      agent.play();
    }
  }
}

function updateAgentAngle(agent, angle) {
  // For testing purposes this is disabled, but when client
  // starts receiving messages concerning agent movements
  // this will be enabled

  // if (agent.angle !== angle) {
  //   for (let index = agent.angle; index <= angle; index++) {
  //     agent.angle += index;
  //   }
  // }

  agent.angle += agent.vAngle;
}

function updateAgentPosition(agent, vx, vy) {
  if (vx === 0 && vy === 0) {
    agentMoving = false;
  } else {
    agentMoving = true;
  }

  // console.log(agentMoving);

  //Apply the velocity values to the idle shooter's
  //position to make it move
  agent.x += vx;
  agent.y += vy;
}

function updateProjectiles(projectileList, speed) {
  for (let index = 0; index < projectileList.length; index++) {
    currentProjectile = projectileList[index];
    currentProjectile.position.x +=
      Math.cos(currentProjectile.rotation) * speed;
    currentProjectile.position.y +=
      Math.sin(currentProjectile.rotation) * speed;

    if (
      currentProjectile.position.x < PLAYABLE_AREA_X_MIN ||
      currentProjectile.position.x > PLAYABLE_AREA_X_MAX ||
      currentProjectile.position.y < PLAYABLE_AREA_Y_MIN ||
      currentProjectile.position.y > PLAYABLE_AREA_Y_MAX
    ) {
      currentProjectile.dead = true;
    }

    if (currentProjectile.dead) {
      currentProjectile.visible = false;
      app.stage.removeChild(currentProjectile);
    }
  }
}

function keyboard(value) {
  const key = {};
  key.value = value;
  key.isDown = false;
  key.isUp = true;
  key.press = undefined;
  key.release = undefined;
  //The `key pressed handler`
  key.downHandler = (event) => {
    if (event.key === key.value) {
      if (key.isUp && key.press) {
        key.press();
      }
      key.isDown = true;
      key.isUp = false;
      event.preventDefault();
    }
  };

  //The `key released handler`
  key.upHandler = (event) => {
    if (event.key === key.value) {
      if (key.isDown && key.release) {
        key.release();
      }
      key.isDown = false;
      key.isUp = true;
      event.preventDefault();
    }
  };

  //Attach event listeners
  const downListener = key.downHandler.bind(key);
  const upListener = key.upHandler.bind(key);

  window.addEventListener("keydown", downListener, false);
  window.addEventListener("keyup", upListener, false);

  // Detach event listeners
  key.unsubscribe = () => {
    window.removeEventListener("keydown", downListener);
    window.removeEventListener("keyup", upListener);
  };

  return key;
}

function moveShooter(shooter) {
  //Capture the keyboard arrow keys
  const left = keyboard("ArrowLeft"),
    up = keyboard("ArrowUp"),
    right = keyboard("ArrowRight"),
    down = keyboard("ArrowDown"),
    angleLeft = keyboard("e"),
    angleRight = keyboard("q");

  //Left arrow key `press` method
  left.press = () => {
    //Change the shooter's velocity when the key is pressed
    shooter.vx = -2;
    // shooter.vy = 0;
  };

  //Left arrow key `release` method
  left.release = () => {
    //If the left arrow has been released, and the right arrow isn't down,
    //and the shooter isn't moving vertically:
    //Stop the shooter
    if (!right.isDown) {
      shooter.vx = 0;
    }
  };

  //Up
  up.press = () => {
    shooter.vy = -2;
    // shooter.vx = 0;
  };

  up.release = () => {
    if (!down.isDown) {
      shooter.vy = 0;
    }
  };

  //Right
  right.press = () => {
    shooter.vx = 2;
    // shooter.vy = 0;
  };

  right.release = () => {
    if (!left.isDown) {
      shooter.vx = 0;
    }
  };

  //Down
  down.press = () => {
    shooter.vy = 2;
    // shooter.vx = 0;
  };

  down.release = () => {
    if (!up.isDown) {
      shooter.vy = 0;
    }
  };

  //angle left
  angleLeft.press = () => {
    shooter["vAngle"] = -2;

    console.log(agent.vAngle);
    // shooter.vx = 0;
  };

  angleLeft.release = () => {
    if (!angleRight.isDown) {
      shooter["vAngle"] = 0;
    }
  };

  //angle right
  angleRight.press = () => {
    shooter["vAngle"] = 2;
    // shooter.vx = 0;
  };

  angleRight.release = () => {
    if (!angleLeft.isDown) {
      shooter["vAngle"] = 0;
    }
  };
}

function createSpriteFromSheet(path, x, y, width, height) {
  let texture = TextureCache[path];
  let textureRect = new Rectangle(x, y, width, height);
  texture.frame = textureRect;
  let sprite = new Sprite(texture);
  return sprite;
}

function fireProjectile(agent) {
  const space = keyboard(" ");

  space.press = () => {
    createProjectile(agent.rotation, {
      x: agent.position.x,
      y: agent.position.y,
    });
  };

  space.release = () => {};
}

function createProjectile(rotation, startPosition) {
  agent.stop();
  agent.textures = agentSheet.spritesheet.animations["survivor-idle_handgun"];
  agent.loop = false;
  agent.animationSpeed = 1;
  agent.play();

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
  projectile.position.x = startPosition.x;
  projectile.position.y = startPosition.y;
  projectile.rotation = rotation;

  projectileList.push(projectile);
  app.stage.addChild(projectile);
}

function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}
