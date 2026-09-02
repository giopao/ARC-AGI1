from __future__ import annotations
import numpy as np


# location of point
class Point:
    def __init__(
        self,
        row: int,
        col: int,
        color: int
    ):
        self.row = row
        self.col = col
        self.color = color


class Rectangle:
    def __init__(
        self,
        top_row: int,
        left_column: int,
        bottom_row: int,
        right_column: int,
        colors: set[int],
        corners_found: int
    ):
        self.top_row = top_row
        self.left_column = left_column
        self.bottom_row = bottom_row
        self.right_column = right_column

        self.colors = colors
        self.corners_found = corners_found

    # Find all positions inside the rectangle
    def get_inside_positions(self):
        inside_positions = []
        for row in range(self.top_row + 1, self.bottom_row):
            for column in range(self.left_column + 1, self.right_column):
                inside_positions.append((row, column))
        return inside_positions

    # Check if point is inside the rectangle
    def is_point_inside(self, point: Point):
        row_is_inside = (self.top_row < point.row < self.bottom_row)
        column_is_inside = (self.left_column < point.col < self.right_column)
        return row_is_inside and column_is_inside
    
def get_colored_positions(grid):
    colored_positions = []
    rows, columns = grid.shape
    for row in range(rows):
        for column in range(columns):
            if grid[row, column] != 0:
                colored_positions.append((row, column, int(grid[row, column])))
    return colored_positions

grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0],
    [0, 2, 0, 2, 0],
    [0, 2, 2, 2, 0],
    [0, 0, 0, 0, 0]
])

# Find positions of all colored cells
positions = get_colored_positions(grid)
print(positions)
