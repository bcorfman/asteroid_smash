import os
import random

from cocos.actions import Repeat, RotateBy, WrappedMove
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite


class Asteroid:
    def __init__(self):
        self.window_width = None

    def start(self):
        self.window_width, self.window_height = (
            director._window_virtual_width,
            director._window_virtual_height,
        )
        buffer = 100
        self.sprite.position = (
            random.randint(buffer, self.window_width - buffer),
            random.randint(buffer, self.window_height - buffer),
        )
        self.sprite.scale = 2


class Small(Asteroid):
    def __init__(self, layer: Layer):
        super(Asteroid, self).__init__()
        img_name = random.choice(["meteorgrey_small1.png", "meteorgrey_small2.png"])
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        Asteroid.start(self)
        self.sprite.velocity = (
            random.choice([-1, 1]) * random.randint(4, 10),
            random.choice([-1, 1]) * random.randint(4, 10),
        )
        self.sprite.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(3, 10))
            )
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)


class Medium(Asteroid):
    def __init__(self, layer: Layer):
        super(Asteroid, self).__init__()
        img_name = random.choice(["meteorgrey_med1.png", "meteorgrey_med2.png"])
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        Asteroid.start(self)
        self.sprite.velocity = (
            random.choice([-1, 1]) * random.randint(3, 9),
            random.choice([-1, 1]) * random.randint(3, 9),
        )
        self.sprite.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(4, 12))
            )
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)


class Large(Asteroid):
    def __init__(self, layer: Layer):
        super(Asteroid, self).__init__()
        img_name = random.choice(
            [
                "meteorgrey_big1.png",
                "meteorgrey_big2.png",
                "meteorgrey_big3.png",
                "meteorgrey_big4.png",
            ]
        )
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        Asteroid.start(self)
        self.sprite.velocity = (
            random.choice([-1, 1]) * random.randint(15, 30),
            random.choice([-1, 1]) * random.randint(15, 30),
        )
        self.sprite.do(
            Repeat(
                RotateBy(random.choice([-1, 1]) * 360, duration=random.randint(5, 15))
            )
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)
