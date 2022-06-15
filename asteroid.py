import arcade
import math
import os
import random
from typing import cast
from arcade.gl.enums import MIN

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroid Smash"
OFFSCREEN_SPACE = 300
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
MIN_ASTEROIDS = 3
MAX_ASTEROIDS = 7
BIG = 3
MEDIUM = 2
SMALL = 1
TINY = 0


class TurningSprite(arcade.Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """
    def __init__(self, filename):
        scale = 0.75
        super().__init__(filename, scale)    
    
    def on_update(self):
        """ Move the sprite """
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class Asteroid(arcade.Sprite):
    def __init__(self, size):
        self.size = size
        if size == BIG:
            idx = random.randint(1, 4)
            sz = 'big'
        elif size in [MEDIUM, SMALL, TINY]:
            idx = random.randint(1, 2)
            sz = ['tiny', 'small', 'med'][size]
        filename = f":resources:images/space_shooter/meteorGrey_{sz}{idx}.png"
        
        scale = 0.75
        super().__init__(filename, scale)
        
        self.easing_angle_data = None
        self.rotation = 0   
        self.setup()    
        
    def setup(self):
        self.rotation = random.randint(1, 5)
        self.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
        self.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
        self.change_x = random.random() * 2 - 1
        self.change_y = random.random() * 2 - 1
        self.change_angle = (random.random() - 0.5) * 2

    def on_update(self, delta_time=1/60.0):
        self.angle += self.rotation
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If the ship goes off-screen, move it to the other side of the window
        if self.right < 0:
            self.left = SCREEN_WIDTH

        if self.left > SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.top = SCREEN_HEIGHT

        if self.top > SCREEN_HEIGHT:
            self.bottom = 0

        super().update()

    def hit(self, asteroids):
        if self.size in [BIG, MEDIUM, SMALL]:
            asteroid_1 = Asteroid(self.size - 1)
            asteroid_2 = Asteroid(self.size - 1)
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
    def __init__(self, filename):
        scale = 0.5
        super().__init__(filename, scale)
        
        self.easing_angle_data = None

        # Info on where we are going.
        # Angle comes in automatically from the parent class.
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0

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
        #else:
            # Handle if there are no joysticks.
            #print("There are no game controllers available. Please plug one in and run again.")
            #self.controller = None
        
        # Mark that we are respawning.
        self.respawn()
        
    def respawn(self):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0
    
    def on_update(self, delta_time=1/60.0):
        if self.easing_angle_data is not None:
            done, self.angle = arcade.ease_angle_update(self.easing_angle_data, delta_time)
            if done:
                self.easing_angle_data = None
        
        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        # If the ship goes off-screen, move it to the other side of the window
        if self.right < 0:
            self.left = SCREEN_WIDTH

        if self.left > SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.top = SCREEN_HEIGHT

        if self.top > SCREEN_HEIGHT:
            self.bottom = 0

        """ Call the parent class. """
        super().on_update()



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
        self.asteroids = None
        self.shots = None
        self.powerups = None
        self.enemies = None
        self.lives = None
        self.scores = None
        
        self.player = None
        self.background_color = None
        self.num_asteroids = MIN_ASTEROIDS
        self.score = 0
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.last_nearest = None
        self.num_lives = 3

        # Sounds
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.hit_sound2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.hit_sound3 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.hit_sound4 = arcade.load_sound(":resources:sounds/hit2.wav")

    def setup(self):
        """ Set up the game and initialize the variables. """
        arcade.set_background_color(arcade.color.BLACK)

        self.asteroids = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.powerups = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.lives = arcade.SpriteList()

        # Set up the player
        self.player = Player(":resources:images/space_shooter/playerShip1_orange.png")
        self.player.angle = 0
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2
        
        for _ in range(self.num_asteroids):
            asteroid = Asteroid(BIG)
            self.asteroids.append(asteroid)

    def on_update(self, delta_time=1/60.0):
        """ Movement and game logic """
        # update player angle data to turn toward nearest asteroid. 
        # actual turning occurs during player.update()
        asteroid, _ = arcade.get_closest_sprite(self.player, self.asteroids)
        if asteroid != self.last_nearest:
            end_angle = -arcade.get_angle_degrees(self.player.center_x, self.player.center_y,
                                                  asteroid.center_x, asteroid.center_y)
            self.player.easing_angle_data = arcade.ease_angle(self.player.angle,
                                                              end_angle,
                                                              rate=800,
                                                              ease_function=arcade.smoothstep)            
            
        for bullet in self.bullets:
            asteroids = arcade.check_for_collision_with_list(bullet, self.asteroid_list)

            for asteroid in asteroids:
                # expected AsteroidSprite, got Sprite instead
                self.split_asteroid(cast(Asteroid, asteroid))
                asteroid.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

            # Remove bullet if it goes off-screen
            size = max(bullet.width, bullet.height)
            if bullet.center_x < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_x > SCREEN_WIDTH + size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y < 0 - size:
                bullet.remove_from_sprite_lists()
            if bullet.center_y > SCREEN_HEIGHT + size:
                bullet.remove_from_sprite_lists()

        if not self.player.respawning:
            collisions = arcade.check_for_collision_with_list(self.player, self.asteroids)
            if collisions:
                if self.lives > 0:
                    self.lives -= 1
                    self.player.respawn()
                    asteroid = collisions[0]
                    self.split_asteroid(cast(Asteroid, asteroids))
                    asteroid.remove_from_sprite_lists()
                    self.ship_life_list.pop().remove_from_sprite_lists()
                    print("Crash")
                else:
                    self.game_over = True
                    print("Game over")

        # Update the text objects
        #self.text_score.text = f"Score: {self.score}"
        #self.text_asteroid_count.text = f"Asteroid Count: {len(self.asteroid_list)}"
        
        self.player.on_update()
        self.asteroids.on_update()
        self.bullets.on_update()
        self.powerups.on_update()
        self.enemies.on_update()
        self.lives.on_update()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player.draw()
        self.asteroids.draw()
        self.bullets.draw()
        self.powerups.draw()
        self.enemies.draw()
        self.lives.draw()

    def on_key_press(self, symbol, modifiers):
        """ Called whenever a key is pressed. """
        # Shoot if the player hit the space bar and we aren't respawning.
        if not self.player.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = TurningSprite(":resources:images/space_shooter/"
                                          "laserBlue01.png")
            bullet_sprite.guid = "Bullet"

            bullet_speed = 13
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.bullet_list.append(bullet_sprite)

            arcade.play_sound(self.laser_sound, speed=random.random() * 3 + 0.5)

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = -.2

    def on_key_release(self, symbol, modifiers):
        """ Called whenever a key is released. """
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = 0

    def split_asteroid(self, asteroid: Asteroid):
        """ Split an asteroid into chunks. """
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 4:
            for _ in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]

                enemy_sprite = Asteroid(image_list[image_no])

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound1.play()

        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]

                enemy_sprite = Asteroid(image_list[image_no])

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound2.play()

        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]

                enemy_sprite = Asteroid(image_list[image_no])

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound3.play()

        elif asteroid.size == 1:
            self.hit_sound4.play()


def main():
    window = Game()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()