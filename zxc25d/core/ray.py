import math
from .math2d import Vec2


class RayHit:
    __slots__ = ("distance", "map_x", "map_y", "side")

    def __init__(self, distance, map_x, map_y, side):
        self.distance = distance
        self.map_x = map_x
        self.map_y = map_y
        self.side = side  # 0 = hit x-side, 1 = hit y-side

    def __repr__(self):
        return (
            f"<RayHit dist={self.distance:.3f} "
            f"cell=({self.map_x},{self.map_y}) side={self.side}>"
        )


class Ray:
    __slots__ = (
        "origin",
        "direction",
        "delta_dist",
        "step",
        "side_dist"
    )

    def __init__(self, origin: Vec2, direction: Vec2):
        self.origin = origin
        self.direction = direction.normalized()

        self.delta_dist = Vec2(
            abs(1.0 / self.direction.x) if self.direction.x != 0 else float("inf"),
            abs(1.0 / self.direction.y) if self.direction.y != 0 else float("inf"),
        )

        self.step = Vec2()
        self.side_dist = Vec2()

    def cast(self, world, max_distance=50.0) -> RayHit | None:
        map_x = int(self.origin.x)
        map_y = int(self.origin.y)

        if self.direction.x < 0:
            self.step.x = -1
            self.side_dist.x = (self.origin.x - map_x) * self.delta_dist.x
        else:
            self.step.x = 1
            self.side_dist.x = (map_x + 1.0 - self.origin.x) * self.delta_dist.x

        if self.direction.y < 0:
            self.step.y = -1
            self.side_dist.y = (self.origin.y - map_y) * self.delta_dist.y
        else:
            self.step.y = 1
            self.side_dist.y = (map_y + 1.0 - self.origin.y) * self.delta_dist.y

        distance = 0.0
        side = 0

        while distance < max_distance:
            if self.side_dist.x < self.side_dist.y:
                self.side_dist.x += self.delta_dist.x
                map_x += int(self.step.x)
                side = 0
            else:
                self.side_dist.y += self.delta_dist.y
                map_y += int(self.step.y)
                side = 1

            if world.is_wall(map_x, map_y):
                if side == 0:
                    distance = self.side_dist.x - self.delta_dist.x
                else:
                    distance = self.side_dist.y - self.delta_dist.y

                return RayHit(distance, map_x, map_y, side)

        return None

