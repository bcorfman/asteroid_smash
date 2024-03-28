import os
import random

from cocos.actions import Repeat, RotateBy, WrappedMove
from cocos.collision_model import CircleShape
from cocos.director import director
from cocos.euclid import Point2, Vector2
from cocos.particle_systems import Color, Explosion
from cocos.sprite import Sprite


class Asteroid(Sprite):
    def __init__(self, image):
        Sprite.__init__(self, image)
        self.buffer = min(self.width, self.height)
        self.window_width, self.window_height = (
            director._window_virtual_width,
            director._window_virtual_height,
        )
        self.scale = 2
        self.generate_position()
        self.cshape = CircleShape(
            Vector2(self.position[0], self.position[1]), self.buffer
        )
        self.colliding = False

    # TODO: this always generates points around the whole landscape, rather than next to a destroyed asteroid.
    def generate_position(self):
        self.position = (
            random.randint(self.buffer, self.window_width - self.buffer),
            random.randint(self.buffer, self.window_height - self.buffer),
        )

    def update_cshape(self):
        self.cshape.center = Vector2(self.position[0], self.position[1])

    def process_collision(self, pt, explosion_size, new_asteroids):
        exp = Explosion()
        exp.auto_remove_on_finish = True
        exp.position = pt
        exp.life = 1.0
        exp.life_var = 0.2
        exp.size = explosion_size
        exp.size_var = 2.0
        exp.start_color = Color(0.5, 0.5, 0.5, 1.0)
        exp.start_color_var = Color(0.0, 0.0, 0.0, 0.0)
        exp.end_color = Color(0.45, 0.45, 0.45, 1.0)
        exp.end_color_var = Color(0.02, 0.02, 0.02, 0.0)
        exp.gravity = Point2(0, 0)
        exp.color_modulate = True
        return exp, new_asteroids


class Small(Asteroid):
    def __init__(self):
        img_name = random.choice(["meteorgrey_small1.png", "meteorgrey_small2.png"])
        image_file = os.path.join("res", img_name)
        Asteroid.__init__(self, image_file)
        self.action = None

    def begin_move(self):
        self.velocity = (
            random.choice([-1, 1]) * random.randint(4, 10),
            random.choice([-1, 1]) * random.randint(4, 10),
        )
        self.action = self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(3, 36))
            )
            | WrappedMove(self.window_width, self.window_height)
        )

    def process_collision(self, pt):
        new_asteroids = []
        return Asteroid.process_collision(self, pt, 2, new_asteroids)


class Medium(Asteroid):
    def __init__(self):
        img_name = random.choice(["meteorgrey_med1.png", "meteorgrey_med2.png"])
        image_file = os.path.join("res", img_name)
        Asteroid.__init__(self, image_file)
        self.action = None

    def begin_move(self):
        self.velocity = (
            random.choice([-1, 1]) * random.randint(3, 9),
            random.choice([-1, 1]) * random.randint(3, 9),
        )
        self.action = self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(4, 48))
            )
            | WrappedMove(self.window_width, self.window_height)
        )

    def process_collision(self, pt):
        new_asteroids = [Small(), Small()]
        return Asteroid.process_collision(self, pt, 4.5, new_asteroids)


class Large(Asteroid):
    def __init__(self):
        img_name = random.choice(
            [
                "meteorgrey_big1.png",
                "meteorgrey_big2.png",
                "meteorgrey_big3.png",
                "meteorgrey_big4.png",
            ]
        )
        image_file = os.path.join("res", img_name)
        Asteroid.__init__(self, image_file)
        self.action = None

    def begin_move(self):
        self.velocity = (
            random.choice([-1, 1]) * random.randint(15, 30),
            random.choice([-1, 1]) * random.randint(15, 30),
        )
        self.action = self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(5, 60))
            )
            | WrappedMove(self.window_width, self.window_height)
        )

    def process_collision(self, pt):
        new_asteroids = [Medium(), Medium()]
        return Asteroid.process_collision(self, pt, 7.0, new_asteroids)
