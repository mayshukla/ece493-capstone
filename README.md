# ECE 493 Capstone Project

## Installation

1. Clone repo

```bash
git clone https://github.com/mayshukla/ece493-capstone.git
cd ece493-capstone
```

1. Install python requirements

```bash
python3 -m pip install -r src/requirements.txt
```

1. Start server.

```bash
python3 -m src <port>
```

1. Go to `localhost:<port>` in a web browser.

## Running tests

1. Follow the first two steps under "Installation" to clone the repo and install python requirements.

1. Install a recent version of Chromium on your machine. See <https://www.chromium.org/getting-involved/download-chromium/>
   This is required since we use the selenium webdriver for chromium to test the frontend.

1. Install additional python requirments for tests.
```
python3 -m pip install -r test/requirements.txt
```

1. Run the following in the root directory of this repo.

```
python3 -m unittest
```

## Sprites and Spritesheets

All sprites were obtained from the following links below under the CC-BY 3.0 and OGA-BY 3.0 licenses

https://www.dlf.pt/pngsn/47299/
https://opengameart.org/content/frostcrest-props-crates-nes
https://opengameart.org/content/animated-top-down-survivor-player
https://github.com/kittykatattack/learningPixi/blob/master/examples/images/dungeon.png
