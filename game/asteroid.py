import os
import random

from cocos.actions import MoveBy, Repeat, RotateBy, WrappedMove
from cocos.collision_model import CircleShape
from cocos.director import director
from cocos.euclid import Vector2
from cocos.sprite import Sprite


class _Asteroid(Sprite):
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

    # Note: this generates points around the whole screen minus a small buffer,
    # so the asteroid is fully visible at the start.
    def generate_position(self):
        self.position = (
            random.randint(self.buffer, self.window_width - self.buffer),
            random.randint(self.buffer, self.window_height - self.buffer),
        )

    def update_cshape(self):
        self.cshape.center = Vector2(self.position[0], self.position[1])

    def begin_move(self):
        print(self.rotation_time)
        self.velocity = self.move_delta
        self.action = self.do(
            Repeat(MoveBy(self.move_delta, duration=1.0))
            | Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=self.rotation_time)
            )
            | WrappedMove(self.window_width, self.window_height)
        )


class SmallAsteroid(_Asteroid):
    def __init__(self):
        image_file = random.choice(["meteorgrey_small1.png", "meteorgrey_small2.png"])
        _Asteroid.__init__(self, image_file)
        self.action = None
        self.size = 1
        self.calc_velocity_and_rotation()

    def calc_velocity_and_rotation(self):
        self.move_delta = (
            random.choice([-1, 1]) * random.randint(50, 120),
            random.choice([-1, 1]) * random.randint(50, 120),
        )
        self.rotation_time = random.randint(2, 8)


class MediumAsteroid(_Asteroid):
    def __init__(self):
        image_file = random.choice(["meteorgrey_med1.png", "meteorgrey_med2.png"])
        _Asteroid.__init__(self, image_file)
        self.action = None
        self.size = 2
        self.calc_velocity_and_rotation()

    def calc_velocity_and_rotation(self):
        self.move_delta = (
            random.choice([-1, 1]) * random.randint(10, 80),
            random.choice([-1, 1]) * random.randint(10, 80),
        )
        self.rotation_time = random.randint(4, 15)


class LargeAsteroid(_Asteroid):
    def __init__(self):
        image_file = random.choice(
            [
                "meteorgrey_big1.png",
                "meteorgrey_big2.png",
                "meteorgrey_big3.png",
                "meteorgrey_big4.png",
            ]
        )
        _Asteroid.__init__(self, image_file)
        self.action = None
        self.size = 3
        self.calc_velocity_and_rotation()

    def calc_velocity_and_rotation(self):
        self.move_delta = (
            random.choice([-1, 1]) * random.randint(5, 35),
            random.choice([-1, 1]) * random.randint(5, 35),
        )
        self.rotation_time = random.randint(5, 30)
