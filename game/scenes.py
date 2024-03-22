import math

from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from cocos.euclid import Vector2
from cocos.layer import ColorLayer
from cocos.sprite import Sprite

from .asteroid import Large


class AttractMode(ColorLayer):
    is_event_handler = True
    max_asteroids = 8

    def __init__(self):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = []
        for _ in range(self.max_asteroids):
            new = Large(self)
            while True:
                collision = False
                for a in self.asteroids:
                    # if new asteroid is too close to existing asteroids, generate another
                    dist = math.hypot(
                        abs(new.position[0] - a.position[0]),
                        abs(new.position[1] - a.position[1]),
                    )
                    if dist <= a.buffer * 2:
                        new.generate_position()
                        collision = True
                        break
                if not collision:
                    self.asteroids.append(new)
                    break
        for a in self.asteroids:
            a.begin_move()

        cell_side = self.asteroids[0].cshape.r * 2
        self.collman = CollisionManagerGrid(
            0.0,
            director._window_virtual_width,
            0.0,
            director._window_virtual_height,
            cell_side,
            cell_side,
        )
        self.schedule(self.update)

    def update(self, dt):
        # add all child objects to collision manager
        self.collman.clear()
        for _, node in self.children:
            self.collman.add(node)

        # mark collisions for processing
        actor: Sprite = None
        other: Sprite = None
        for actor, other in self.collman.iter_all_collisions():
            actor.colliding = True
            other.colliding = True
            actor.remove_action(actor.action)
            other.remove_action(other.action)

        # process collisions
        for _, item in enumerate(reversed(self.asteroids), start=1):
            if item.colliding:
                item.colliding = False
                self.asteroids.remove(item)
                self.remove(item)

        # update cshapes for next frame
        for asteroid in self.asteroids:
            asteroid.update_cshape()
