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
        color: int
    ):
        self.top_row = top_row
        self.left_column = left_column
        self.bottom_row = bottom_row
        self.right_column = right_column
        self.color = color

    # Find all cells that are inside the rectangle
    def get_inside_positions(self):
        inside_cells = []
        for row in range(self.top_row + 1, self.bottom_row):
            for column in range(self.left_column + 1, self.right_column):
                inside_cells.append((row, column))
        return inside_cells

    # Check whether a point is inside the rectangle
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