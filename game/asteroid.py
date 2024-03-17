import os
import random

from cocos.actions import Repeat, RotateBy
from cocos.sprite import Sprite


class Small:
    def __init__(self):
        img_name = random.choice("meteorgrey_small1.png", "meteorgrey_small2.png")
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)

    def start(self):
        self.sprite.do(Repeat(RotateBy(360, duration=random.randint(3, 10))))


class Medium:
    def __init__(self):
        img_name = random.choice("meteorgrey_med1.png", "meteorgrey_med2.png")
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)

    def start(self):
        self.sprite.do(Repeat(RotateBy(360, duration=random.randint(4, 12))))


class Large:
    def __init__(self):
        img_name = random.choice(
            "meteorgrey_big1.png",
            "meteorgrey_big2.png",
            "meteorgrey_big3.png",
            "meteorgrey_big4.png",
        )
        image_file = os.path.join("res", img_name)
        self.sprite = Sprite(image_file)

    def start(self):
        self.sprite.do(Repeat(RotateBy(360, duration=random.randint(5, 15))))
