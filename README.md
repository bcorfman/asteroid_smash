# Asteroid Smash

An jazzed-up version of Asteroids designed with Cocos2D.

## Prerequisites
* At a command prompt in the project directory, type `make devinstall` to set up the project in development mode, or just `make install` to set up the game as runnable only.

## To run the game
* At a command prompt in the project directory, type `make run`.

## Game instructions
* Left-arrow and right-arrow move the ship left and right. 
* Down-arrow to thrust in the direction the ship is facing.
* Left-CTRL or right-CTRL to fire your laser.
* Spacebar to hyperspace.
* Catch random power-ups when they randomly cross the screen to briefly improve your ship's capabilites.
* Hit the `ESC` key to quit the game.
* Yes, it's a prototype.

## Notes for Visual Studio Code users
* I've included some extension recommendations that can make your development easier.
  * [Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave)
  * [Make support and task provider](https://marketplace.visualstudio.com/items?itemName=carlos-algms.make-task-provider)
* These recommendations will pop up when opening the project inside VSCode.
* Installing both extensions will
  * Use the code in `settings.json` to run `make format` on each `File:Save`.
  * Display available Make targets within the _Makefile Tasks_ sidebar pane and allow them to be run with a mouse click.

## To do
* Keep developing the gameplay.