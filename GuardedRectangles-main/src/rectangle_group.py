# from src.point import Point
from rectangle import Rectangle
from utils.logger import logger

class RectangleGroup:
    """Manages a collection of Rectangles and Points.  
    All ids are ints

    point_to_rect: set of all the rectangles touching this point
    """
    def __init__(self):
        self.rectangles: dict[int, Rectangle] = {}
        self.points: dict[tuple[int, int], int] = {}
        self.point_to_rect: dict[tuple[int, int], set[int]] = {}

    def add_rectangle(self, rect_id:int):
        if rect_id in self.rectangles:
            msg = f"Rectangle_ID {rect_id} already exists in group."
            logger.error(msg)
            raise KeyError(msg)
        
        self.rectangles[rect_id] = Rectangle(rect_id)
        
    def add_point(self, rect_id:int, label:int, x:int, y:int):
        point = (x, y)

        if point in self.points:
            # previously seen point
            self.point_to_rect[point].add(rect_id)
        else:
            # new point
            self.point_to_rect[point] = set()
            self.point_to_rect[point].add(rect_id)
            self.points[point] = label
        
        self.rectangles[rect_id].add_point(x,y)


    def compute_adjacencies(self):
        """Populates the adjacency graph for all rectangles in this group.
        For rectangle adjaceny, rectangles are nodes and the edges are { rect.adj | rect in self.rectangles } 
        """
        rect_list = list(self.rectangles.values())
        
        # NOTE: O(n . m^2) ~ O(16n) complexity. Only needs to run once per block. 
        # n - number of points
        # m - number of rectangles that share a point; 1 <= m <= 4 (For out use case, m <= 3)
        for point in self.point_to_rect:
            for rect_id in self.point_to_rect[point]:
                for other in self.point_to_rect[point]:
                    if rect_id != other:
                        # mark as neighbour in both rectangles
                        self.rectangles[rect_id].adj.add(other)
                        self.rectangles[other].adj.add(rect_id)