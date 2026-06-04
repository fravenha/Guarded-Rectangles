from typing import TextIO

from rectangle_group import RectangleGroup
from utils.logger import logger

class ProblemParser:
    """Provides functions that read the input dataset and construct RectangleGroups.

    Expected Input format:  
    num_groups  
    num_rectangles_in_group1  
    1 num_points x1 y1 x2 y2 ... x_num_points y_num_points  
    2 num_points x1 y1 x2 y2 ... x_num_points y_num_points   
    ...  
    num_rectangles_in_group1 num_points x1 y1 x2 y2 ... x_num_points y_num_points  
    num_rectangles_in_group2  
    ...
    """
    @staticmethod
    def parse_block(file: TextIO) -> RectangleGroup:
        line = file.readline()
        
        group = RectangleGroup()
        
        if not line:
            raise ValueError("Unexpected epmty line at the start of this group.")
            
        num_rectangles = int(line)

        point_id_counter = 0

        for _ in range(num_rectangles):
            # Read rectangle data for this group
            # Line format: rect_id num_points x1 y1 x2 y2 ...
            line = file.readline()
            arr = line.split()

            rect_id = int(arr[0])
            group.add_rectangle(rect_id)

            num_points = int(arr[1]) 
            
            if (num_points < 4):
                raise ValueError(f"Unexpected number of points in rectangle: {num_points}")

            for i in range(num_points):
                point_id_counter = point_id_counter + 1
                group.add_point(
                    rect_id = rect_id,
                    label = point_id_counter, 
                    x = int( arr[2 + i*2]), 
                    y = int( arr[2 + i*2 + 1]),
                )

        group.compute_adjacencies()
        logger.debug(f"New group:\nRects - {len(group.rectangles)}\n")
        return group
                
    @staticmethod
    def parse_all(file_path:str) -> list[RectangleGroup]:
        """Read file and return all the RectangleGroups"""
        logger.info(f"Reading and parsing '{file_path}' ...") 
        try:       
            groups = []
            with open(file_path, 'r') as file:
                line = file.readline()
                
                num_groups = int(line)

                # start index at 1
                for _ in range(num_groups):
                    group = ProblemParser.parse_block(file)
                    groups.append(group)

            return groups
        except FileNotFoundError:
            logger.error(f"Error: The file was not found:{file_path}\n")
            return []
