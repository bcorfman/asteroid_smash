import math

from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from cocos.layer import ColorLayer

from .asteroid import Large


class AttractMode(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = []
        count = 0
        while True:
            new = Large(self)
            for a in self.asteroids:
                # if new asteroid is too close to existing asteroids, generate another
                if (
                    math.hypot(
                        new.position[0] - a.position[0], new.position[1] - a.position[1]
                    )
                    <= 100
                ):
                    continue
            self.asteroids.append(new)
            count += 1
            if count >= 8:
                break

        cell_side = self.asteroids[0].cshape.r * 2
        self.collman = CollisionManagerGrid(
            0.0,
            director._window_virtual_width,
            0.0,
            director._window_virtual_height,
            cell_side,
            cell_side,
        )
        print(repr(a))
        for a in self.asteroids:
            self.collman.add(a)
