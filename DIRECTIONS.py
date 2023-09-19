class Directions():
    NORTH = "n"
    SOUTH = "s"
    WEST = "w"
    EAST = "e"

    def turnLeft(self) -> str:
        return {
            "n": "w",
            "e": "n",
            "s": "e",
            "w": "s",
        }[self]

    def turnRight(self) -> str:
        return {
            "n": "e",
            "e": "s",
            "s": "w",
            "w": "n",
        }[self]

