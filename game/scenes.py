from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from cocos.layer import ColorLayer

from .asteroid import Large


class AttractMode(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = [Large(self) for _ in range(8)]
        cell_side = self.asteroids[0].cshape.r * 2
        self.collman = CollisionManagerGrid(
            0.0,
            director._window_virtual_width,
            0.0,
            director._window_virtual_height,
            cell_side,
            cell_side,
        )
        for a in self.asteroids:
            self.collman.add(a)
