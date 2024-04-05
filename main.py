import os

import pyglet
from cocos.director import director
from cocos.scene import Scene

from game.scenes import AttractMode

pyglet.resource.path.append(os.path.join(os.path.dirname(__file__), "res"))
pyglet.resource.reindex()


def main():
    director.init(width=1920, height=1400, caption="Asteroid Smash")
    director.run(Scene(AttractMode()))


if __name__ == "__main__":
    main()
