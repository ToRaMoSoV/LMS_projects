import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt

from .map_grid import MapGrid
from .palette import Palette
from zxc25d.runtime.runtime import run


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZXC25D Map Editor")
        self.resize(900, 600)

        self.current_file = None

        self.grid = MapGrid(20, 20)
        self.palette = Palette()

        self.palette.symbol_changed.connect(self.grid.set_current_symbol)

        central = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.palette)
        layout.addWidget(self.grid)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self._create_menu()

    def _create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = file_menu.addAction("Open")
        save_action = file_menu.addAction("Save")
        save_as_action = file_menu.addAction("Save As")
        run_action = file_menu.addAction("Run")

        open_action.triggered.connect(self.open_map)
        save_action.triggered.connect(self.save_map)
        save_as_action.triggered.connect(self.save_map_as)
        run_action.triggered.connect(self.run_game)

    def open_map(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open map", "", "Map files (*.map)"
        )
        if not path:
            return

        try:
            self.grid.load_from_file(path)
            self.current_file = path
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_map(self):
        if not self.current_file:
            self.save_map_as()
            return

        self.grid.save_to_file(self.current_file)

    def save_map_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save map", "", "Map files (*.map)"
        )
        if not path:
            return

        if not path.endswith(".map"):
            path += ".map"

        self.current_file = path
        self.grid.save_to_file(path)

    def run_game(self):
        if not self.current_file:
            QMessageBox.warning(self, "Run", "Save map first")
            return

        run(self.current_file)


def main():
    app = QApplication(sys.argv)
    window = EditorWindow()
    window.show()
    sys.exit(app.exec())

