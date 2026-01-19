from dataclasses import dataclass
from .map import Map


@dataclass
class Entity:
    kind: str
    x: float
    y: float


class World:
    def __init__(self, game_map: Map):
        self.map = game_map
        self.entities: list[Entity] = []
        self.player_start: tuple[float, float] | None = None

        self._extract_entities()

    def _extract_entities(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                tile = self.map.grid[y][x]
                ch = tile.char

                if ch == "P":
                    self.player_start = (x + 0.5, y + 0.5)
                    tile.char = "."
                    tile.solid = False

                elif ch == "E":
                    self.entities.append(
                        Entity("enemy", x + 0.5, y + 0.5)
                    )
                    tile.char = "."
                    tile.solid = False

                elif ch == "H":
                    self.entities.append(
                        Entity("health", x + 0.5, y + 0.5)
                    )
                    tile.char = "."
                    tile.solid = False

    def get_entities_by_kind(self, kind: str):
        return [e for e in self.entities if e.kind == kind]

    def is_wall(self, x: int, y: int) -> bool:
        return self.map.is_wall(x, y)

    def __repr__(self):
        return (
            f"<World {self.map.width}x{self.map.height}, "
            f"entities={len(self.entities)}, "
            f"player_start={self.player_start}>"
        )

