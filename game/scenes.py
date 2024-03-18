import cocos

from .asteroid import Large


class AttractMode(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = [Large(self) for _ in range(8)]
        for a in self.asteroids:
            a.start()
