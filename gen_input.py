import random

def is_valid(grid, row, col, num, N, box_height, box_width):
    if num in grid[row] or num in [grid[i][col] for i in range(N)]:
        return False

    box_start_row = (row // box_height) * box_height
    box_start_col = (col // box_width) * box_width

    for i in range(box_height):
        for j in range(box_width):
            if grid[box_start_row + i][box_start_col + j] == num:
                return False
    return True

def generate_complete_board(size,box_height, box_width):
    board = [[0 for _ in range(size)] for _ in range(size)]
    def fill():
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    nums = list(range(1, size+1))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, i, j, num,size,box_height, box_width):
                            board[i][j] = num
                            if fill():
                                return True
                            board[i][j] = 0
                    return False
        return True

    fill()
    return board

def generate_puzzle(level,size,box_height, box_width):
    """
    Sinh puzzle dựa trên bảng đã hoàn chỉnh.
    Cấp độ tương ứng với số ô gợi ý:
      1: Basic        -> 40 clues
      2: Easy         -> 36 clues
      3: Intermediate -> 32 clues
      4: Advance      -> 28 clues
      5: Extreme      -> 24 clues
      6: Evil         -> 22 clues
    """
    mapping = {1: 40, 2: 36, 3: 32, 4: 28, 5: 24, 6: 22}
    clues = mapping.get(level, 40)
    complete_board = generate_complete_board(size,box_height, box_width)
    puzzle = [row[:] for row in complete_board]
    total_cells = size*size
    cells_to_remove = total_cells - clues

    positions = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(positions)
    for i in range(cells_to_remove):
        r, c = positions[i]
        puzzle[r][c] = 0

    return puzzle, complete_board

def generate_input(level,size):
    """
    Sinh ra puzzle ngẫu nhiên theo cấp độ, ghi vào file input/<level>_gen.txt (chữ thường).
    Trả về puzzle và solution.
    """
    if size == 9:
        box_height, box_width = 3, 3
    elif size == 12:
        box_height, box_width = 3, 4
    elif size == 16:
        box_height, box_width = 4, 4
    else:
        raise ValueError("Chỉ hỗ trợ Sudoku 12x12 hoặc 16x16")
    level_names = {1: "basic", 2: "easy", 3: "intermediate",
                   4: "advance", 5: "extreme", 6: "evil"}
    puzzle, solution = generate_puzzle(level,size,box_height, box_width)
    filename = f"input/{level_names.get(level, 'basic')}_{size}x{size}_gen.txt"
    with open(filename, "w") as f:
        for row in puzzle:
            line = " ".join(str(num) for num in row)
            f.write(line + "\n")
    return puzzle, solution
