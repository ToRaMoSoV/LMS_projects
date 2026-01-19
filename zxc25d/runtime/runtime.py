import arcade

from zxc25d.core.map import Map
from zxc25d.core.world import World
from zxc25d.core.camera import Camera
from zxc25d.core.raycaster import Raycaster


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ZXC25D Diagnostic Runtime"


class DiagnosticRuntime(arcade.Window):
    def __init__(self, map_path: str):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            resizable=False
        )

        self.world = World(Map.load(map_path))
        self.camera = Camera(*self.world.player_start)

        self.raycaster = Raycaster(SCREEN_WIDTH)

        self.keys = set()

        arcade.set_background_color((20, 20, 20))


    def on_key_press(self, key, modifiers):
        self.keys.add(key)

    def on_key_release(self, key, modifiers):
        self.keys.discard(key)


    def on_update(self, dt):
        move = 0.0
        strafe = 0.0
        rot = 0.0

        speed = self.camera.move_speed * dt
        rot_speed = self.camera.rot_speed * dt

        if arcade.key.W in self.keys:
            move += speed
        if arcade.key.S in self.keys:
            move -= speed
        if arcade.key.A in self.keys:
            strafe -= speed
        if arcade.key.D in self.keys:
            strafe += speed

        if arcade.key.LEFT in self.keys:
            rot -= rot_speed
        if arcade.key.RIGHT in self.keys:
            rot += rot_speed

        self.camera.rotate(rot)
        self.camera.move(move, strafe, self.world)

    def on_draw(self):
        self.clear()

        rays = self.raycaster.cast_all(self.camera, self.world)

        column_width = SCREEN_WIDTH / len(rays)
        center_y = SCREEN_HEIGHT // 2

        for r in rays:
            wall_height = int(SCREEN_HEIGHT * r.wall_height)

            y1 = center_y - wall_height // 2
            y2 = center_y + wall_height // 2

            shade = 180 if r.side == 0 else 130

            arcade.draw_lrbt_rectangle_filled(
                r.column * column_width,
                r.column * column_width + column_width,
                y1,
                y2,
                (shade, shade, shade)
            )


def run(map_path: str):
    DiagnosticRuntime(map_path)
    arcade.run()

