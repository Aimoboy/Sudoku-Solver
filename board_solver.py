from board import *
from tile import *
from solution_data import *
import time

class BoardSolver:
    def load_board(self, board):
        self.board = board.copy()
        self.backtracks = 0
    
    def set_certain_tiles(self, board):
        is_changed = True
        while is_changed:
            is_changed = False

            # Length of possibility list is one
            for i in range(board.dimension):
                for j in range(board.dimension):
                    tile = board.tiles[i][j]
                    if len(tile.possibilities) == 1:
                        board.set_tile(tile.possibilities[0], i, j)
                        is_changed = True
            
            # A number appears once in a possibility list in a group
            for i in range(board.group_cols):
                for j in range(board.group_rows):
                    group = board.get_group(i, j)
                    for k in range(1, board.dimension + 1):
                        found = 0
                        found_tile = None
                        for t in group:
                            if t.number == k:
                                break
                            if k in t.possibilities:
                                found += 1
                                found_tile = t
                        if found == 1:
                            board.set_tile(k, found_tile.row, found_tile.col)
                            is_changed = True
            
            # Check for one possibility in a row
            for i in range(board.dimension):
                for j in range(1, board.dimension + 1):
                    found = 0
                    found_tile = None
                    for k in range(board.dimension):
                        t = board.tiles[i][k]
                        if t.number == j:
                            break
                        if j in t.possibilities:
                            found += 1
                            found_tile = t
                    if found == 1:
                        board.set_tile(j, found_tile.row, found_tile.col)
                        is_changed = True
            
            # Check for one possibility in a column
            for i in range(board.dimension):
                for j in range(1, board.dimension + 1):
                    found = 0
                    found_tile = None
                    for k in range(board.dimension):
                        t = board.tiles[k][i]
                        if t.number == j:
                            break
                        if j in t.possibilities:
                            found += 1
                            found_tile = t
                    if found == 1:
                        board.set_tile(j, found_tile.row, found_tile.col)
                        is_changed = True

    def check_solution(self, board):
        # Check that all tiles have zero possibilities
        for i in range(board.dimension):
            for j in range(board.dimension):
                t = board.tiles[i][j]
                if len(t.possibilities) != 0:
                    return False
        
        # Check that each group have one of each number
        for i in range(board.group_cols):
            for j in range(board.group_rows):
                group = board.get_group(i, j)
                for k in range(1, board.dimension + 1):
                    found = 0
                    for t in group:
                        if t.number == k:
                            found += 1
                    if found != 1:
                        return False
        
        # Check that each row have one of each number
        for i in range(board.dimension):
            for j in range(1, board.dimension + 1):
                found = 0
                for k in range(board.dimension):
                    t = board.tiles[i][k]
                    if t.number == j:
                        found += 1
                if found != 1:
                    return False
        
        # Check that each col have one of each number
        for i in range(board.dimension):
            for j in range(1, board.dimension + 1):
                found = 0
                for k in range(board.dimension):
                    t = board.tiles[k][i]
                    if t.number == j:
                        found += 1
                if found != 1:
                    return False
        
        return True

    def recursive_solve(self, board):
        self.set_certain_tiles(board)

        # Make list of missing tiles
        missing_tiles = list()
        for i in range(board.dimension):
            for j in range(board.dimension):
                t = board.tiles[i][j]
                if t.number == 0:
                    missing_tiles.append(t)
        
        # Solution found
        if len(missing_tiles) == 0:
            if not self.check_solution(board):
                raise Exception("Wrong board was found to be the solution.")
            self.board = board
            return True

        # Invalid tile
        for t in missing_tiles:
            if len(t.possibilities) == 0:
                self.backtracks += 1
                return False
        
        # Sort tiles by amount of possibilities
        missing_tiles.sort(key=lambda t: len(t.possibilities))

        tile = missing_tiles[0]
        for i in range(len(tile.possibilities)):
            board_copy = board.copy()
            board_copy.set_tile(tile.possibilities[i], tile.row, tile.col)

            ret_val = self.recursive_solve(board_copy)

            if ret_val:
                return True
        
        return False

    def find_solution(self):
        start_time = time.time()

        # Remove possibilities from start tiles
        for i in range(self.board.dimension):
            for j in range(self.board.dimension):
                t = self.board.tiles[i][j]
                self.board.remove_possibilities(t.row, t.col)
        
        ret_val = self.recursive_solve(self.board)
        elapsed_time = time.time() - start_time

        return SolutionData(ret_val, self.board, elapsed_time, self.backtracks)
