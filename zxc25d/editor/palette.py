from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class Palette(QWidget):
    symbol_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.current_symbol = "#"

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Palette")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        self.buttons = {}

        for symbol, name, color in [
            ("#", "Wall (#)", QColor(120, 120, 120)),
            (".", "Empty (.)", QColor(50, 50, 50)),
            ("P", "Player (P)", QColor(0, 200, 0)),
            ("E", "Enemy (E)", QColor(200, 50, 50)),
            ("H", "Health (H)", QColor(50, 150, 255)),
        ]:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color.name()};
                    color: black;
                    padding: 6px;
                }}
                QPushButton:checked {{
                    border: 3px solid yellow;
                }}
                """
            )
            btn.clicked.connect(lambda checked, s=symbol: self.select_symbol(s))
            layout.addWidget(btn)
            self.buttons[symbol] = btn

        self.buttons[self.current_symbol].setChecked(True)

        layout.addStretch()
        self.setLayout(layout)

    def select_symbol(self, symbol: str):
        self.current_symbol = symbol

        for s, btn in self.buttons.items():
            btn.setChecked(s == symbol)

        self.symbol_changed.emit(symbol)

