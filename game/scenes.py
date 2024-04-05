import math

from cocos.collision_model import CollisionManagerGrid
from cocos.director import director
from cocos.euclid import Point2, Vector2
from cocos.layer import ColorLayer
from cocos.particle_systems import Color, Explosion
from cocos.sprite import Sprite

from .asteroid import LargeAsteroid, MediumAsteroid, SmallAsteroid

SMALL, MEDIUM, LARGE = range(3)


class AttractMode(ColorLayer):
    is_event_handler = True
    max_asteroids = 8

    def __init__(self, schedule_update=True):
        super(AttractMode, self).__init__(0, 0, 0, 255)
        self.asteroids = self.generate_asteroids()
        for a in self.asteroids:
            a.begin_move()
            self.add(a)
        self.asteroid_dims = [
            (s.width, s.height)
            for s in [SmallAsteroid(), MediumAsteroid(), LargeAsteroid()]
        ]
        cell_side = min(self.asteroid_dims[LARGE]) * 1.25
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
        asteroids = [LargeAsteroid()]
        for _ in range(1, self.max_asteroids):
            new = LargeAsteroid()
            while True:
                collision = False
                for a in asteroids:
                    # if new asteroid is too close to existing asteroids, generate another
                    dist = math.hypot(
                        abs(new.position[0] - a.position[0]),
                        abs(new.position[1] - a.position[1]),
                    )
                    if dist <= a.buffer * 1.5:
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
            actor.remove_action(actor.action)
            other.remove_action(other.action)
            midpt = self.calc_midpoint(actor.cshape.center, other.cshape.center)
            self.asteroids.remove(actor)
            self.asteroids.remove(other)
            self.process_collision(actor, other, midpt)
            self.remove(actor)
            self.remove(other)

        # update cshapes for next frame
        for asteroid in self.asteroids:
            asteroid.update_cshape()

    def calc_midpoint(self, vec1: Vector2, vec2: Vector2):
        return (vec1.x + vec2.x) / 2, (vec1.y + vec2.y) / 2

    def process_collision(self, asteroid1, asteroid2, pt):
        sz = self.break_asteroids(asteroid1, asteroid2, pt)
        self.generate_explosion(pt, sz)

    def break_asteroids(self, asteroid1, asteroid2, pt):
        # Break larger colliding asteroids into smaller pieces.
        # If an asteroid is already small, it just vanishes.
        new_asteroids = []
        sz = 1
        for a in [asteroid1, asteroid2]:
            if a.size == 3:
                new_asteroids.extend([MediumAsteroid(), MediumAsteroid()])
            elif a.size == 2:
                new_asteroids.extend([SmallAsteroid(), SmallAsteroid()])
        if new_asteroids:
            sz = (asteroid1.size + asteroid2.size) / 2.0
            # Calc new asteroid positions based on the largest
            # side of a medium asteroid, which gives a little extra distance.
            offset = max(self.asteroid_dims[SMALL]) * 1.25
            positions = [
                (pt[0] + offset, pt[1] + offset),
                (pt[0] - offset, pt[1] + offset),
                (pt[0] - offset, pt[1] - offset),
                (pt[0] + offset, pt[1] - offset),
            ]

            # New asteroids will go in opposite directions to
            # each other in order to avoid any immediate collisions.
            coeff = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
            for i, a in enumerate(new_asteroids):
                a.position = positions[i]
                a.move_delta = (
                    coeff[i][0] * abs(a.move_delta[0]),
                    coeff[i][1] * abs(a.move_delta[1]),
                )
                a.begin_move()
                self.add(a)
            print("---")
            self.asteroids.extend(new_asteroids)
        return sz

    def generate_explosion(self, pt, sz):
        exp = Explosion()
        exp.auto_remove_on_finish = True
        exp.position = pt
        exp.life = 0.5
        exp.life_var = 0.2
        exp.size = 7.0 * sz
        exp.size_var = 2.0
        exp.start_color = Color(0.5, 0.5, 0.5, 1.0)
        exp.start_color_var = Color(0.0, 0.0, 0.0, 0.0)
        exp.end_color = Color(0.45, 0.45, 0.45, 1.0)
        exp.end_color_var = Color(0.02, 0.02, 0.02, 0.0)
        exp.gravity = Point2(0, 0)
        exp.color_modulate = True
        self.add(exp)
