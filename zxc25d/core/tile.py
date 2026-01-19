class Tile:
    __slots__ = ("char", "solid")

    def __init__(self, char: str):
        self.char = char
        self.solid = self._is_solid(char)

    @staticmethod
    def _is_solid(char: str) -> bool:
        return char not in (".", " ")

    def is_wall(self) -> bool:
        return self.solid

    def __repr__(self):
        return f"Tile('{self.char}', solid={self.solid})"

