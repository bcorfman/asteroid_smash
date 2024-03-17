import os
import random

import cocos
from cocos.actions import Repeat, RotateBy, WrappedMove
from cocos.director import director
from cocos.sprite import Sprite


class Asteroid:
    def __init__(self, _: cocos.layer.Layer):
        self.window_width = None

    def start(self):
        self.window_width, self.window_height = (
            director._window_virtual_width,
            director._window_virtual_height,
        )
        self.sprite.position = (
            random.randint(0, self.window_width),
            random.randint(0, self.window_height),
        )


class Small:
    def __init__(self, layer: cocos.layer.Layer):
        img_name = random.choice("meteorgrey_small1.png", "meteorgrey_small2.png")
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        super(Asteroid, self).__init__()
        self.sprite.velocity = random.randint(4, 10), random.randint(4, 10)
        self.sprite.do(
            Repeat(RotateBy(360, duration=random.randint(3, 10)))
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)


class Medium:
    def __init__(self, layer: cocos.layer.Layer):
        img_name = random.choice("meteorgrey_med1.png", "meteorgrey_med2.png")
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        super(Asteroid, self).__init__()
        self.sprite.velocity = random.randint(3, 9), random.randint(3, 9)
        self.sprite.do(
            Repeat(RotateBy(360, duration=random.randint(4, 12)))
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)


class Large:
    def __init__(self, layer: cocos.layer.Layer):
        img_name = random.choice(
            "meteorgrey_big1.png",
            "meteorgrey_big2.png",
            "meteorgrey_big3.png",
            "meteorgrey_big4.png",
        )
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)
        self._layer = layer

    def start(self):
        super(Asteroid, self).__init__()
        self.sprite.velocity = random.randint(2, 8), random.randint(2, 8)
        self.sprite.do(
            Repeat(RotateBy(360, duration=random.randint(5, 15)))
            | WrappedMove(self.window_width, self.window_height)
        )
        self._layer.add(self.sprite)
