from .tile import Tile


class Map:
    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height

    @classmethod
    def load(cls, path: str):
        with open(path, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        if not lines:
            raise ValueError("Map file is empty")

        width = len(lines[0])
        for line in lines:
            if len(line) != width:
                raise ValueError("All map lines must have the same length")

        grid = []
        for y, line in enumerate(lines):
            row = []
            for x, ch in enumerate(line):
                row.append(Tile(ch))
            grid.append(row)

        return cls(grid, width, len(grid))

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def tile_at(self, x: int, y: int) -> Tile:
        if not self.in_bounds(x, y):
            raise IndexError("Tile out of bounds")
        return self.grid[y][x]

    def is_wall(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return True
        return self.grid[y][x].is_wall()

    def __repr__(self):
        return f"<Map {self.width}x{self.height}>"

