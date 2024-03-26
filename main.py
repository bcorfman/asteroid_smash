import os

from cocos.director import director
from cocos.scene import Scene

from game.scenes import AttractMode

PROJECT_DIR = os.path.dirname(__file__)


def main():
    director.init(width=1024, height=768, caption="Asteroid Smash")
    director.run(Scene(AttractMode()))


if __name__ == "__main__":
    main()
