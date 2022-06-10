import arcade
import os
import random

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroid Smash"
BIG = 3
MEDIUM = 2
SMALL = 1
TINY = 0


class Asteroid(arcade.Sprite):
    def __init__(self, size, scale):
        self.size = size
        if size == BIG:
            idx = random.randint(1, 4)
            sz = 'big'
        elif size in [MEDIUM, SMALL, TINY]:
            idx = random.randint(1, 2)
            sz = ['tiny', 'small', 'med'][size]
        filename = f":resources:images/space_shooter/meteorGrey_{sz}{idx}.png"
        
        super().__init__(filename, scale)
        
        self.easing_angle_data = None
        self.velocity = 0 
        self.rotation = 0       
        
    def setup(self):
        self.velocity = random.randint(1, 10)
        self.rotation = random.randint(1, 5)

    def on_update(self, asteroids: arcade.SpriteList, delta_time: float = 1 / 60):
        self.angle += self.rotation
            
    def hit(self, asteroids):
        if self.size in [BIG, MEDIUM, SMALL]:
            asteroid_1 = Asteroid(self.size - 1, SPRITE_SCALING)
            asteroid_2 = Asteroid(self.size - 1, SPRITE_SCALING)
            asteroid_1.center_x = asteroid_2.center_x = self.center_x
            asteroid_1.center_y = asteroid_2.center_y = self.center_y
            asteroid_1.setup()
            asteroid_2.setup()
            asteroids.append(asteroid_1)
            asteroids.append(asteroid_2)
        # play sound
        # emit particles
        self.kill()        


class Player(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        
        self.easing_angle_data = None
        
        # Get list of game controllers that are available
        controllers = arcade.get_game_controllers()

        # If we have any...
        if controllers:
            # Grab the first one in  the list
            self.controller = controllers[0]

            # Open it for input
            self.controller.open()

            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.controller.push_handlers(self)
        else:
            # Handle if there are no joysticks.
            print("There are no game controllers available. Please plug one in and run again.")
            self.controller = None

    def on_update(self, asteroids: arcade.SpriteList, delta_time: float = 1 / 60):
        asteroid, dist = arcade.get_closest_sprite(self, asteroids)
        
        if self.easing_angle_data is not None:
            done, self.angle = arcade.ease_angle_update(self.easing_angle_data, delta_time)
            if done:
                self.easing_angle_data = None


class Game(arcade.Window):
    """Main application class."""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player = None
        self.asteroids = None
        self.powerups = None
        self.shots = None
        self.enemies = None
        self.background_color = None

        self.score = 0
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0

    def setup(self):
        """ Set up the game and initialize the variables. """
        arcade.set_background_color(arcade.color.BLACK)

        self.players = arcade.SpriteList()
        self.asteroids = arcade.SpriteList()
        self.shots = arcade.SpriteList()
        self.aliens = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        self.scores = arcade.SpriteList()

        # Set up the player
        player = Player(":resources:images/space_shooter/playerShip1_orange.png", SPRITE_SCALING)
        player.angle = 0
        player.center_x = SCREEN_WIDTH / 2
        player.center_y = SCREEN_HEIGHT / 2
        self.players.append(player)
        
        for _ in random.randint(3, 7):
            asteroid = Asteroid(BIG, SPRITE_SCALING)
            self.asteroids.append(asteroid)

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.asteroids.on_update(delta_time)
        self.player.on_update(self.asteroids, delta_time)


def main():
    window = Game()
    window.setup()
    arcade.run()