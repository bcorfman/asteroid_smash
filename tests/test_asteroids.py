import pyglet

pyglet.options["headless"] = True

import math
import os

from cocos.director import director

from game.scenes import AttractMode

director.init()


def test_generate_asteroids():
    project_dir = os.path.dirname(__file__)
    print(project_dir)
    scene = AttractMode(project_dir)
    for i in range(len(scene.asteroids) - 1):
        for j in range(i + 1, len(scene.asteroids)):
            p1 = scene.asteroids[i].position
            p2 = scene.asteroids[j].position
            assert (
                math.hypot(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
                > scene.asteroids[i].buffer * 2
            )
