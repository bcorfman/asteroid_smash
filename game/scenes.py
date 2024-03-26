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

    def __init__(self, schedule_update=True):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = self.generate_asteroids()
        for a in self.asteroids:
            a.begin_move()
            self.add(a)

        cell_side = self.asteroids[0].cshape.r * 2
        self.collman = CollisionManagerGrid(
            0.0,
            director._window_virtual_width,
            0.0,
            director._window_virtual_height,
            cell_side,
            cell_side,
        )
        if schedule_update:
            self.schedule(self.update)

    def generate_asteroids(self):
        asteroids = []
        for _ in range(self.max_asteroids):
            new = Large()
            while True:
                collision = False
                for a in asteroids:
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
                    asteroids.append(new)
                    break
        return asteroids

    def update(self, dt):
        # add all child objects to collision manager
        self.collman.clear()
        for node in self.asteroids:
            self.collman.add(node)

        # mark collisions for processing
        actor: Sprite = None
        other: Sprite = None
        for actor, other in self.collman.iter_all_collisions():
            actor.colliding = True
            actor.remove_action(actor.action)
            other.remove_action(other.action)
            midpt = self.calc_midpoint(actor.cshape.center, other.cshape.center)

        # process collisions
        for _, item in enumerate(reversed(self.asteroids), start=1):
            if item.colliding:
                print("collision")
                item.colliding = False
                explosion = item.process_collision(midpt)
                self.add(explosion)
                self.asteroids.remove(item)
                self.remove(item)

        # update cshapes for next frame
        for asteroid in self.asteroids:
            asteroid.update_cshape()

    def calc_midpoint(self, vec1: Vector2, vec2: Vector2):
        return (vec1.x + vec2.x) / 2, (vec1.y + vec2.y) / 2
