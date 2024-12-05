from enum import Enum

type Coordinate = tuple[int, int]

class Direction(Enum):
    Up = 1
    DiagonalRightUp = 5
    Right = 2
    DiagonalRightDown = 6
    Down = 3
    DiagonalLeftDown = 7
    Left = 4
    DiagonalLeftUp = 8

    def __repr__(self) -> str:

        match self:
            case Direction.Up:
                return "⬆"
            case Direction.DiagonalRightUp:
                return "↗️"
            case Direction.Right:
                return "➔"
            case Direction.DiagonalRightDown:
                return "↘️"
            case Direction.Down:
                return "⬇"
            case Direction.DiagonalLeftDown:
                return "↙️"
            case Direction.Left:
                return "⬅"
            case Direction.DiagonalLeftUp:
                return "↖️"
            case _:
                return super().__repr__()


    @staticmethod
    def GetUpwardsDirections() -> set:
        return set([Direction.DiagonalRightUp, Direction.Up, Direction.DiagonalLeftUp])

    @staticmethod
    def GetDownwardsDirections() -> set:
        return set([Direction.DiagonalRightDown, Direction.Down, Direction.DiagonalLeftDown])

    @staticmethod
    def GetLeftwardsDirections() -> set:
        return set([Direction.DiagonalLeftUp, Direction.Left, Direction.DiagonalLeftDown])

    @staticmethod
    def GetRightwardsDirections() -> set:
        return set([Direction.DiagonalRightUp, Direction.Right, Direction.DiagonalRightDown])