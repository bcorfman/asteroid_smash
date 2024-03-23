# Asteroid Smash

An jazzed-up version of Asteroids designed with Cocos2D.

## Prerequisites
* Cocos2D has dependencies on SDL2 for sound and OpenGL for graphics. To [set](https://github.com/microsoft/WSL/issues/2855) [these](https://github.com/microsoft/WSL/discussions/9350) [up](https://installati.one/install-libsdl1.2-dev-ubuntu-22-04/) correctly on WSL2/Ubuntu, type `make prereq` at an Ubuntu shell prompt. (I can't promise things will work exactly the same on your WSL2/Ubuntu version, but the code and links should hopefully provide you with enough guidance to get to a working state.)
* Once the OS-level prerequisites are installed, type `make devinstall` to set up the project-level dependencies in development mode, or just `make install` to set up the game as runnable only.

## To run the tests (provided you've done `make devinstall` above)
* At a command prompt in the project directory, type `make tests`.

## To run the game
* At a command prompt in the project directory, type `make run`.

## Notes for Visual Studio Code users
* I've included some extension recommendations that can make your development easier.
  * [Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave)
  * [Make support and task provider](https://marketplace.visualstudio.com/items?itemName=carlos-algms.make-task-provider)
* These recommendations will pop up when opening the project inside VSCode.
* Installing both extensions will
  * Use the code in `settings.json` to run `make format` on each `File:Save`.
  * Display available Make targets within the _Makefile Tasks_ sidebar pane and allow them to be run with a mouse click.

## Game instructions
* The game starts in attract mode.
* Hit the `ESC` key to quit the game.
* Yes, it's a prototype. 

## To do
* Left-arrow and right-arrow move the ship left and right. 
* Down-arrow to thrust in the direction the ship is facing.
* Left-CTRL or right-CTRL to fire your laser.
* Spacebar to hyperspace.
* Catch random power-ups when they randomly cross the screen to briefly improve your ship's capabilities.
