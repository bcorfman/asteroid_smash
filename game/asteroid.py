import os
import random

from cocos.actions import Repeat, RotateBy, WrappedMove
from cocos.collision_model import CircleShape
from cocos.director import director
from cocos.euclid import Vector2
from cocos.layer import Layer
from cocos.particle_systems import Explosion
from cocos.sprite import Sprite


class Asteroid(Sprite):
    def __init__(self, image):
        Sprite.__init__(self, image)
        self.buffer = max(self.width, self.height)
        self.window_width, self.window_height = (
            director._window_virtual_width,
            director._window_virtual_height,
        )
        self.scale = 2
        self.generate_position()
        self.colliding = False

    def generate_position(self):
        self.position = (
            random.randint(self.buffer, self.window_width - self.buffer),
            random.randint(self.buffer, self.window_height - self.buffer),
        )
        self.cshape = CircleShape(
            Vector2(self.position[0], self.position[1]), self.buffer
        )


class Small(Asteroid):
    def __init__(self, layer: Layer):
        self._layer = layer
        img_name = random.choice(["meteorgrey_small1.png", "meteorgrey_small2.png"])
        image_file = os.path.join("res", img_name)
        Asteroid.__init__(self, image_file)
        self.velocity = (
            random.choice([-1, 1]) * random.randint(4, 10),
            random.choice([-1, 1]) * random.randint(4, 10),
        )
        self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(3, 10))
            )
            | WrappedMove(self.window_width, self.window_height)
        )

    def process_collision(self, pt):
        exp = Explosion()
        exp.auto_remove_on_finish = True
        exp.position = pt
        self._layer.add(exp)


class Medium(Asteroid):
    def __init__(self, layer: Layer):
        img_name = random.choice(["meteorgrey_med1.png", "meteorgrey_med2.png"])
        image_file = os.path.join("res", img_name)
        Asteroid.__init__(self, image_file)
        self.velocity = (
            random.choice([-1, 1]) * random.randint(3, 9),
            random.choice([-1, 1]) * random.randint(3, 9),
        )
        self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(4, 12))
            )
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer = layer
        self._layer.add(self)

    def process_collision(self, pt):
        exp = Explosion()
        exp.auto_remove_on_finish = True
        exp.position = pt
        self._layer.add(exp)


class Large(Asteroid):
    def __init__(self, layer: Layer):
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
        self._layer = layer
        self._layer.add(self)

    def begin_move(self):
        self.velocity = (
            random.choice([-1, 1]) * random.randint(15, 30),
            random.choice([-1, 1]) * random.randint(15, 30),
        )
        self.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(5, 15))
            )
            | WrappedMove(self.window_width, self.window_height)
        )

    def process_collision(self, pt):
        exp = Explosion()
        exp.auto_remove_on_finish = True
        exp.position = pt
        self._layer.add(exp)
