//Aliases
const Application = PIXI.Application,
  loader = PIXI.Loader.shared,
  resources = PIXI.Loader.shared.resources,
  Sprite = PIXI.Sprite,
  TextureCache = PIXI.utils.TextureCache,
  Rectangle = PIXI.Rectangle,
  AnimatedSprite = PIXI.AnimatedSprite,
  Container = PIXI.Container,
  ParticleContainer = PIXI.ParticleContainer;

const PI = 3.14;
const PLAYABLE_AREA_X_RIGHT = 1024 - 64;
const PLAYABLE_AREA_X_LEFT = 64;
const PLAYABLE_AREA_Y_UP = 30;
const PLAYABLE_AREA_Y_DOWN = 700 - 30;

//Create a Pixi Application
const app = new Application({
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
  .add("../assets/shooterIdle.json")
  .add("../assets/shooterIdle.png")
  .add("../assets/obstacleboxes.png")
  .add("../assets/obstacleboxes1.png")
  .add("../assets/obstacleboxes2.png")
  .add("../assets/obstacleboxes3.png")
  .add("../assets/obstacleboxes4.png")
  .add("../assets/obstacleboxes5.png")
  .load(setup);

let idleSheet, id, idleAnim, shooterIdle, gameState;

//This `setup` function will run when the image has loaded
function setup() {
  //Create the shooter sprite
  id = resources["../assets/dungeon.json"].textures;
  idleSheet = resources["../assets/shooterIdle.json"];

  //   creating the shooter dude single frame
  const textureIdle = TextureCache["../assets/shooterIdle.png"];

  //Create a rectangle object that defines the position and
  //size of the sub-image you want to extract from the texture
  //(`Rectangle` is an alias for `PIXI.Rectangle`)
  const idleRect = new Rectangle(0, 0, 253, 216);

  //Tell the texture to use that rectangular section
  textureIdle.frame = idleRect;

  //Create the sprite from the texture
  shooterIdle = new Sprite(textureIdle);

  // creating obstacles
  let obstacles = new ParticleContainer(1500, {
    rotation: true,
    tint: true,
    vertices: true,
    uvs: true,
  });

  yellowBox = createSpriteFromSheet("../assets/obstacleboxes.png", 0, 0, 32, 32);
  yellowBox.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  yellowBox.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(yellowBox);

  blueBox = createSpriteFromSheet("../assets/obstacleboxes1.png", 32, 0, 32, 32);
  blueBox.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  blueBox.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(blueBox);

  orangeBox = createSpriteFromSheet("../assets/obstacleboxes2.png", 64, 0, 32, 32);
  orangeBox.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  orangeBox.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(orangeBox);

  greyBox1 = createSpriteFromSheet("../assets/obstacleboxes3.png", 96, 0, 32, 32);
  greyBox1.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  greyBox1.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(greyBox1);

  greyBox2 = createSpriteFromSheet("../assets/obstacleboxes4.png", 128, 0, 32, 32);
  greyBox2.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  greyBox2.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(greyBox2);

  pinkBox = createSpriteFromSheet("../assets/obstacleboxes5.png", 160, 0, 32, 32);
  pinkBox.x = getRndInteger(PLAYABLE_AREA_X_LEFT, PLAYABLE_AREA_X_RIGHT);
  pinkBox.y = getRndInteger(PLAYABLE_AREA_Y_UP, PLAYABLE_AREA_Y_DOWN);
  obstacles.addChild(pinkBox);




  // create an animated sprite from the json sheet in assets
  idleAnim = new AnimatedSprite(
    idleSheet.spritesheet.animations["survivor-idle_handgun"]
  );
  console.log(idleAnim);

  // set speed, start playback and add it to the stage
  idleAnim.animationSpeed = 0.3;
  idleAnim.play();
  idleAnim.x = 65;
  idleAnim.y = 350;
  idleAnim.width = 50;
  idleAnim.height = 50;

  idleAnim.vx = 0;
  idleAnim.vy = 0;

  idleAnim.anchor.set(0.5, 0.5);

  background = new Sprite(id["dungeon.png"]);

  background.scale.set(2, 1.367);
  //   agent size and obstacle size are 50 px
  shooterIdle.width = 50;
  shooterIdle.height = 50;
  shooterIdle.x = 65;
  shooterIdle.y = 30;

  app.stage.addChild(background);
  app.stage.addChild(obstacles);
  //   app.stage.addChild(shooterIdle);
  app.stage.addChild(idleAnim);

  //   Start game loop
  app.ticker.add((delta) => gameLoop(delta));

  // start listening for key input to move shoooter
  moveShooter(idleAnim);

  //   set the game state to play
  gameState = play;
}

function gameLoop(delta) {
    // this calls the play fxn 60 times per minute
    gameState(delta);

}

function play(delta) {
  //Apply the velocity values to the idle shooter's
  //position to make it move
  idleAnim.x += idleAnim.vx;
  idleAnim.y += idleAnim.vy;
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
    down = keyboard("ArrowDown");

  //Left arrow key `press` method
  left.press = () => {
    //Change the shooter's velocity when the key is pressed
    shooter.vx = -1;
    shooter.vy = 0;

    shooter.angle = 180;
  };

  //Left arrow key `release` method
  left.release = () => {
    //If the left arrow has been released, and the right arrow isn't down,
    //and the shooter isn't moving vertically:
    //Stop the shooter
    if (!right.isDown && shooter.vy === 0) {
      shooter.vx = 0;
    }
  };

  //Up
  up.press = () => {
    shooter.vy = -1;
    shooter.vx = 0;
    shooter.angle = 270;
  };

  up.release = () => {
    if (!down.isDown && shooter.vx === 0) {
      shooter.vy = 0;
    }
  };

  //Right
  right.press = () => {
    shooter.vx = 1;
    shooter.vy = 0;
    shooter.angle = 0;
  };

  right.release = () => {
    if (!left.isDown && shooter.vy === 0) {
      shooter.vx = 0;
    }
  };

  //Down
  down.press = () => {
    shooter.vy = 1;
    shooter.vx = 0;
    shooter.angle = 90;
  };

  down.release = () => {
    if (!up.isDown && shooter.vx === 0) {
      shooter.vy = 0;
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

function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}
