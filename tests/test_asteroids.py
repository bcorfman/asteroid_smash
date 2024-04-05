import math
import os

import pyglet

pyglet.options["headless"] = True

from cocos.director import director

from game.scenes import AttractMode

director.init(width=1920, height=1400, caption="Asteroid Smash")


def test_generate_asteroids():
    project_dir = os.path.dirname(os.path.os.path.dirname(__file__))
    pyglet.resource.path.append(os.path.join(project_dir, "res"))
    pyglet.resource.reindex()
    scene = AttractMode()
    for i in range(len(scene.asteroids) - 1):
        for j in range(i + 1, len(scene.asteroids)):
            p1 = scene.asteroids[i].position
            p2 = scene.asteroids[j].position
            assert (
                math.hypot(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
                > scene.asteroids[i].buffer * 1.5
            )
