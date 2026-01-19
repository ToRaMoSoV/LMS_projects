import math
from .math2d import Vec2


class Camera:
    __slots__ = (
        "pos",
        "angle",
        "fov",
        "move_speed",
        "rot_speed"
    )

    def __init__(
        self,
        x: float,
        y: float,
        angle: float = 0.0,
        fov: float = math.pi / 3
    ):
        self.pos = Vec2(x, y)
        self.angle = angle
        self.fov = fov

        self.move_speed = 3.0
        self.rot_speed = 2.5

    @property
    def direction(self) -> Vec2:
        return Vec2(
            math.cos(self.angle),
            math.sin(self.angle)
        )

    @property
    def plane(self) -> Vec2:
        half_fov = self.fov / 2.0
        return Vec2(
            -math.sin(self.angle),
            math.cos(self.angle)
        ) * math.tan(half_fov)

    def rotate(self, delta: float):
        self.angle += delta
        self.angle %= math.tau

    def move(self, forward: float, strafe: float, world):
        dir_vec = self.direction
        right_vec = Vec2(-dir_vec.y, dir_vec.x)

        new_pos = self.pos + dir_vec * forward + right_vec * strafe

        if not world.is_wall(int(new_pos.x), int(self.pos.y)):
            self.pos.x = new_pos.x

        if not world.is_wall(int(self.pos.x), int(new_pos.y)):
            self.pos.y = new_pos.y

