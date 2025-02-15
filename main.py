import os
import time
import tracemalloc
from board import *
from solve import *

def read_sudoku(filename):
    """
    Đọc file và trả về ma trận Sudoku 9x9.
    """
    sudoku = []
    with open(filename, 'r') as file:
        for line in file:
            # Loại bỏ khoảng trắng thừa và ký tự xuống dòng
            line = line.strip()
            # Chuyển các số trong dòng thành list
            row = list(map(int, line.split()))
            sudoku.append(row)
    return sudoku



def main():
    # Ví dụ một bàn Sudoku 9x9 (0 đại diện cho ô trống)
    level = ("basic.txt","easy.txt","intermediate.txt","advance.txt","extreme.txt","evil.txt")
    while True:
        print("\nChọn level:\
          1.Basic\
          2.Easy\
          3.intermediate\
          4.advance\
          5.extreme\
          6.evil")
        inp = int(input())
        if inp in range(1,6): 
            break
    
    file_input = f"input\{level[inp-1]}"
    init_board = read_sudoku(file_input)
    while True:
        print("\nChọn Giải thuật để giải bài toán sudoku:\
            1.DFS\
            2.A*")
        inp = int(input())
        if inp in (1,2):
            break            
    try:
        tracemalloc.start()
        start = time.time()
        board = Board(init_board)
        solve = Solver(board)
        #solve
        if inp == 1:
            if solve.solve_dfs(False):
                print("Giải thành công")
            else:
                print("Không thành công")
        elif inp == 2:
            return        
        
        # tính toán thời gian và bộ nhớ
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        time_run = time.time() - start
        memory_alloc = top_stats[0].size / 1024

        # in kết quả
        print(f"Thời gian: {time_run:.2f}s")
        print(f"Bộ nhớ: {memory_alloc} KB")
        user_input = int(input("Ấn \"1\" để chạy kết quả step-by-step: "))
        if user_input == 1:
            draw_board = Board(init_board)
            draw_solve = Solver(draw_board)
            draw_solve.solve_dfs(drawFlag= True)
            print(f"Thời gian: {time_run:.2f}s")
            print(f"Bộ nhớ: {memory_alloc} KB")
        else:
            return
        
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    main()
    
