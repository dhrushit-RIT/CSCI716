from LineSegment import LineSegment
from Point import Point


class Wall(LineSegment):
    starting_point: Point
    top_end: Point
    bot_end: Point

    def __init__(self, top_end: Point, bot_end: Point, start_point: Point) -> None:
        super().__init__(top_end, bot_end)
        self.top_end = top_end
        self.bot_end = bot_end
        self.starting_point = start_point

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)
