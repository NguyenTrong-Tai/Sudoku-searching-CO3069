import os
import time
import tracemalloc
VALUE = {1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:'A',
        11:'B',
        12:'C',
        13:'D',
        14:"E",
        15:"F"}
class Cell:
    def __init__(self, value):
        self.value = value
        if value != 0:
            self.is_fixed = True  # ô đã được điền
        else:
            self.is_fixed = False

    def set_value(self, new_value):
        if not self.is_fixed:
            self.value = new_value

    def get_value(self):
        return self.value

    def isfixed(self) -> bool:
        return self.is_fixed

class Board:
    def __init__(self, grid_init,size_board = 9):
        # Tạo một lưới size_boardxsize_board gồm các cell
        self.grid = [[Cell(grid_init[row][col]) for col in range(size_board)] for row in range(size_board)]
        self.size_board = int(size_board)

        if self.size_board == 9:
            self.box_height, self.box_width = 3, 3
        elif self.size_board == 12:
            self.box_height, self.box_width = 3, 4
        elif self.size_board == 15:
            self.box_height, self.box_width = 3, 5
    def is_valid_cell(self, row, col, value):
        # Kiểm tra hàng và cột
        for i in range(self.size_board):
            if self.grid[row][i].value == value or self.grid[i][col].value == value:
                return False

        # Kiểm tra ô vuông 3x3, 3x4, 3x5
        box_start_row = (row // self.box_height) * self.box_height
        box_start_col = (col // self.box_width) * self.box_width
        
        for i in range(self.box_height):
            for j in range(self.box_width):
                if self.grid[box_start_row + i][box_start_col + j].value == value:
                    return False
        return True  # valid

    def find_empty_cell(self):
        for row in range(self.size_board):
            for col in range(self.size_board):
                if self.grid[row][col].value == 0:
                    return (row, col)
        return None

    # DRAW BOARD
    def color_text(self, text, color):
        COLORS = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "reset": "\033[0m",
        }
        return f"{COLORS[color]}{text}{COLORS['reset']}"

    def draw_grid(self, row=-1, col=-1):
        box_height,box_width = self.box_height, self.box_width

        def print_horizontal_line():
            print(("+" + "-" * (2 * box_width + 1)) * (self.size_board // box_width) + "+")
    
    
        print_horizontal_line()
        for i in range(self.size_board):
            if i % box_height == 0 and i != 0:
                print_horizontal_line()
            for j in range(self.size_board+1):
                if j % box_width == 0:
                    print("|", end=" ")
                if j != self.size_board:
                    ctx = VALUE[self.grid[i][j].get_value()] if self.grid[i][j].get_value() != 0 else "."
                    
                    if i == row and j == col:
                        print(self.color_text(ctx, 'red'), end=" ")
                    elif self.grid[i][j].isfixed():
                        print(self.color_text(ctx, 'green'), end=" ")
                    else:
                        print(ctx, end=" ")

            print()
        print_horizontal_line()
        print()

    def update_cell_draw(self, row, col, value):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.grid[row][col].set_value(value)
        self.draw_grid(row, col)
        time.sleep(0.15)
