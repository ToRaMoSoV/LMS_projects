import math
from .ray import Ray


class RaycastResult:
    __slots__ = (
        "column",
        "distance",
        "map_x",
        "map_y",
        "side",
        "wall_height"
    )

    def __init__(self, column, distance, map_x, map_y, side, wall_height):
        self.column = column
        self.distance = distance
        self.map_x = map_x
        self.map_y = map_y
        self.side = side
        self.wall_height = wall_height

    def __repr__(self):
        return (
            f"<RaycastResult col={self.column} "
            f"dist={self.distance:.3f} "
            f"cell=({self.map_x},{self.map_y}) side={self.side}>"
        )


class Raycaster:
    def __init__(self, screen_width: int, max_distance: float = 50.0):
        self.screen_width = screen_width
        self.max_distance = max_distance

    def cast_all(self, camera, world) -> list[RaycastResult]:
        results = []

        for column in range(self.screen_width):
            camera_x = 2.0 * column / self.screen_width - 1.0

            ray_dir = (
                camera.direction +
                camera.plane * camera_x
            )

            ray = Ray(camera.pos, ray_dir)
            hit = ray.cast(world, self.max_distance)

            if hit is None:
                continue

            perp_distance = hit.distance * math.cos(
                camera.angle - math.atan2(ray_dir.y, ray_dir.x)
            )

            if perp_distance <= 0:
                continue

            wall_height = 1.0 / perp_distance

            results.append(
                RaycastResult(
                    column=column,
                    distance=perp_distance,
                    map_x=hit.map_x,
                    map_y=hit.map_y,
                    side=hit.side,
                    wall_height=wall_height
                )
            )

        return results

