import random
import time
import os
from board import Board, Cell

class SASolver:
    def __init__(self, board: Board):
        self.board = board
        self.non_fixed = []
        self.size = board.size_board
        for i in range(self.size):
            row_non_fixed = []
            fixed_nums = set()
            for j in range(self.size):
                if self.board.grid[i][j].isfixed():
                    fixed_nums.add(self.board.grid[i][j].value)
                else:
                    row_non_fixed.append(j)
            self.non_fixed.append(row_non_fixed)
            missing = list(set(range(1, self.size + 1)) - fixed_nums)
            random.shuffle(missing)
            for idx, col in enumerate(row_non_fixed):
                self.board.grid[i][col].set_value(missing[idx])

    def compute_total_conflicts(self):
        """
        Tính tổng số mâu thuẫn của bảng hiện tại dựa trên cột và khối 3x3.
        Mỗi cột/khối có mâu thuẫn = self.size - (số giá trị khác nhau).
        """
        total_conflicts = 0
        for col in range(self.size):
            col_values = [self.board.grid[row][col].value for row in range(self.size)]
            total_conflicts += (self.size - len(set(col_values)))

        
        block_height, block_width = self.board.box_height, self.board.box_width

        for block_row in range(self.size // block_height):
            for block_col in range(self.size // block_width):
                block_values = []
                for i in range(block_height):
                    for j in range(block_width):
                        r = block_row * block_height + i
                        c = block_col * block_width + j
                        block_values.append(self.board.grid[r][c].value)
                total_conflicts += (self.size - len(set(block_values)))
        return total_conflicts

    def compute_cell_conflict(self, row, col):
        """
        Tính số mâu thuẫn của một ô (không tính hàng vì hàng luôn hợp lệ).
        Chỉ tính mâu thuẫn ở cột và khối.
        """
        conflict = 0
        val = self.board.grid[row][col].value

        for r in range(self.size):
            if r != row and self.board.grid[r][col].value == val:
                conflict += 1

        block_height, block_width = self.board.box_height, self.board.box_width

        start_row = (row // block_height) * block_height
        start_col = (col // block_width) * block_width

        for i in range(block_height):
            for j in range(block_width):
                r = start_row + i
                c = start_col + j
                if (r != row or c != col) and self.board.grid[r][c].value == val:
                    conflict += 1

        return conflict


    def solve_sa(self, drawFlag=False):
        """
        Sudoku Min-Conflicts :v:
          - Khởi tạo lời giải hoàn chỉnh theo hàng. (có thể đúng hoặc không hên thì đúng không hên thì không)
          - Trong mỗi loop, tính tổng mâu thuẫn (chỉ xét cột và khối).
          - Nếu tổng mâu thuẫn = 0, yessssssssssss.
          - Chọn random 1 hàng có mâu thuẫn và trong hàng đó duyệt qua tất cả các cặp hoán đổi
            (giữa các ô không cố định) để tìm cặp cho kết quả giảm mâu thuẫn tốt nhất.
          - Nếu không tìm được cặp cải thiện, thực hiện hoán đổi random.
          - Nếu drawFlag=True, in bảng sau mỗi 100 bước lặp để theo dõi quá trình giải.
        """
        max_iterations = 1000000
        iteration = 0
        current_conflicts = self.compute_total_conflicts()

        while current_conflicts > 0 and iteration < max_iterations:
            iteration += 1

            conflicted_rows = []
            for row in range(self.size):
                for col in self.non_fixed[row]:
                    if self.compute_cell_conflict(row, col) > 0:
                        conflicted_rows.append(row)
                        break

            if not conflicted_rows:
                break

            row = random.choice(conflicted_rows)
            best_delta = float('inf')
            best_pair = None
            original_conflicts = current_conflicts

            row_non_fixed = self.non_fixed[row]
            for i in range(len(row_non_fixed)):
                for j in range(i + 1, len(row_non_fixed)):
                    c1 = row_non_fixed[i]
                    c2 = row_non_fixed[j]
                    self.board.grid[row][c1].value, self.board.grid[row][c2].value = \
                        self.board.grid[row][c2].value, self.board.grid[row][c1].value
                    new_conflicts = self.compute_total_conflicts()
                    delta = new_conflicts - original_conflicts
                    self.board.grid[row][c1].value, self.board.grid[row][c2].value = \
                        self.board.grid[row][c2].value, self.board.grid[row][c1].value
                    if delta < best_delta:
                        best_delta = delta
                        best_pair = (c1, c2)

            if best_pair is not None and best_delta < 0:
                c1, c2 = best_pair
                self.board.grid[row][c1].value, self.board.grid[row][c2].value = \
                    self.board.grid[row][c2].value, self.board.grid[row][c1].value
            else:
                c1, c2 = random.sample(row_non_fixed, 2)
                self.board.grid[row][c1].value, self.board.grid[row][c2].value = \
                    self.board.grid[row][c2].value, self.board.grid[row][c1].value

            current_conflicts = self.compute_total_conflicts()

            if drawFlag and iteration % 100 == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Iteration: {iteration}, Total Conflicts: {current_conflicts}")
                self.board.draw_grid()
                time.sleep(0.1)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Kết quả cuối cùng:")
        self.board.draw_grid()
        return current_conflicts == 0
