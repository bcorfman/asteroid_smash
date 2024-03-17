import cocos
from asteroid import Large


class GameScene(cocos.layer.ColorLayer):
    def __init__(self):
        super(GameScene, self).__init__(0, 0, 0, 255)
        self.asteroids = []
