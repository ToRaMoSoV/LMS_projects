from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt


class MapGrid(QWidget):
    def __init__(self, width: int, height: int, cell_size: int = 32):
        super().__init__()

        self.map_width = width
        self.map_height = height
        self.cell_size = cell_size

        self.current_symbol = "#"

        self.grid = [
            ["." for _ in range(self.map_width)]
            for _ in range(self.map_height)
        ]

        self.setMinimumSize(
            self.map_width * self.cell_size,
            self.map_height * self.cell_size
        )

        self.setMouseTracking(True)

    #API

    def set_current_symbol(self, symbol: str):
        self.current_symbol = symbol

    def load_from_file(self, path: str):
        with open(path, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        if not lines:
            raise ValueError("Map file is empty")

        width = len(lines[0])
        height = len(lines)

        for line in lines:
            if len(line) != width:
                raise ValueError("Invalid map format")

        self.map_width = width
        self.map_height = height
        self.grid = [list(line) for line in lines]

        self.setMinimumSize(
            self.map_width * self.cell_size,
            self.map_height * self.cell_size
        )

        self.update()

    def save_to_file(self, path: str):
        with open(path, "w") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")


    def mousePressEvent(self, event):
        if event.button() not in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            return

        x = event.position().x()
        y = event.position().y()

        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)

        if not (0 <= grid_x < self.map_width and 0 <= grid_y < self.map_height):
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.grid[grid_y][grid_x] = self.current_symbol
        elif event.button() == Qt.MouseButton.RightButton:
            self.grid[grid_y][grid_x] = "."

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        bg = QColor(30, 30, 30)
        painter.fillRect(self.rect(), bg)

        pen_grid = QPen(QColor(60, 60, 60))
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)

        for y in range(self.map_height):
            for x in range(self.map_width):
                px = x * self.cell_size
                py = y * self.cell_size

                ch = self.grid[y][x]

                if ch != ".":
                    color = self._color_for_symbol(ch)
                    painter.fillRect(
                        px + 1,
                        py + 1,
                        self.cell_size - 2,
                        self.cell_size - 2,
                        color
                    )

                painter.drawRect(
                    px,
                    py,
                    self.cell_size,
                    self.cell_size
                )

    def _color_for_symbol(self, ch: str) -> QColor:
        if ch == "#":
            return QColor(120, 120, 120)
        if ch == "P":
            return QColor(0, 200, 0)
        if ch == "E":
            return QColor(200, 50, 50)
        if ch == "H":
            return QColor(50, 150, 255)
        return QColor(180, 180, 180)

