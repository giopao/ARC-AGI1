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
        number_of_corners: int
    ):
        self.top_row = top_row
        self.left_column = left_column
        self.bottom_row = bottom_row
        self.right_column = right_column

        self.colors = colors
        self.number_of_corners = number_of_corners

    # Find all positions inside the rectangle
    def get_inside_positions(self):
        inside_positions = []
        for row in range(self.top_row + 1, self.bottom_row):
            for column in range(self.left_column + 1, self.right_column):
                inside_positions.append((row, column))
        return inside_positions

    # Check if point is inside the rectangle
    def point_inside(self, point: Point):
        row_inside = (self.top_row < point.row < self.bottom_row)
        column_inside = (self.left_column < point.col < self.right_column)
        return row_inside and column_inside
    
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

def find_rectangles(grid):
    number_rectangles = []
    number_of_rows, number_of_columns = grid.shape

    # Test every pair of rows
    for top_row in range(number_of_rows):
        for bottom_row in range(top_row + 1, number_of_rows):

            # Test every pair of columns
            for left_column in range(number_of_columns):
                for right_column in range(left_column + 1, number_of_columns):

                    corner_positions = [(top_row, left_column),
                        (top_row, right_column),
                        (bottom_row, left_column),
                        (bottom_row, right_column)]

                    number_of_corners = 0
                    rectangle_colors = set()

                    # Detect corners which are colored
                    for row, column in corner_positions:
                        color = int(grid[row, column])

                        if color != 0:
                            number_of_corners += 1
                            rectangle_colors.add(color)

                    # Minimum requirement for rectangle 
                    if number_of_corners >= 3:
                        rectangle = Rectangle(
                            top_row,
                            left_column,
                            bottom_row,
                            right_column,
                            rectangle_colors,
                            number_of_corners)

                        number_rectangles.append(rectangle)

    return number_rectangles

rectangles = find_rectangles(grid)

for rectangle in rectangles:
    print(
        "Rectangle found:",
        "top row =", rectangle.top_row,
        "left column =", rectangle.left_column,
        "bottom row =", rectangle.bottom_row,
        "right column =", rectangle.right_column,
        "colors =", rectangle.colors,
        "number of corners =", rectangle.number_of_corners)
