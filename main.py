from cocos.director import director
from cocos.scene import Scene

from game.scenes import AttractMode


def main():
    director.init(width=1920, height=1080, caption="Asteroid Smash")
    director.run(Scene(AttractMode()))


if __name__ == "__main__":
    main()
