INFINITY = float('inf')
NEG_INF = float('-inf')

class Rectangle:
    """Represents a rectangle defined by its ID and bounding coordinates."""
    def __init__(self, rect_id: int):
        self.id = rect_id
        
        # Bounding coordinates
        # x bounds
        self.left = INFINITY
        self.right = NEG_INF
        # y bounds
        self.bottom = INFINITY
        self.top = NEG_INF

        self.is_covered: bool = False
        
        # Collections for graph logic
        self.points: set[tuple[int, int]] = set() 
        """Set of the (x,y) tuples representing the vertices in this rectangle's perimeter."""
        self.adj: set[int] = set() 
        """IDs of adjacent touching rectangles"""

    def bl(self):
        """Coordinates of `Bottom Left` corner of this Rectangle"""
        return (self.left, self.bottom)
    def tr(self):
        """Coordinates of `Top Right` corner of this Rectangle"""
        return (self.right, self.top)
    
    def add_point(self, x:int, y:int):
        self.points.add((x,y))

        if(self.top == NEG_INF):
            self.top = y
            self.bottom = y
            self.right = x
            self.left = x

        if (x > self.right):
            self.right = x
        elif (x < self.left):
            self.left = x
            
        if (y > self.top):
            self.top = y
        elif ( y < self.bottom):
            self.bottom = y
    
    # NOTE: Use RectangleGroup.point_to_rectangle and Rectangle.adj instead
    # def is_touching_rect(self, other: 'Rectangle') -> bool:
    #     """Checks if this rectangle shares an edge boundary with another."""
    #     # Check vertical edge sharing
    #     if (self.left == other.right) or (self.right == other.left):
    #         in_bound = (self.bottom <= other.bottom <= self.top) or (self.bottom <= other.top <= self.top) or \
    #                    (other.bottom <= self.bottom <= other.top)
    #         if in_bound:
    #             return True
                
    #     # Check horizontal edge sharing
    #     elif (self.top == other.bottom) or (self.bottom == other.top):
    #         in_bound = (self.left <= other.right <= self.right) or (self.left <= other.left <= self.right) or \
    #                    (other.left <= self.left <= other.right)
    #         if in_bound:
    #             return True

    #     return False

    def __repr__(self):
        return f"Rect {self.id}: BL=({self.left},{self.bottom}), TR=({self.right},{self.top}), Adj={self.adj}"