from tile import *

class Board:
    def __init__(self, group_rows=3, group_cols=3, board_start=None):
        self.group_rows = group_rows
        self.group_cols = group_cols
        self.dimension = group_rows * group_cols

        # Make tiles
        self.tiles = list()
        for i in range(self.dimension):
            tmp = list()
            for j in range(self.dimension):
                tmp.append(Tile(i, j))
            self.tiles.append(tmp)
        
        # Make groups
        self.tile_groups = list()
        for i in range(self.group_cols):
            tmp = list()
            for j in range(self.group_rows):
                tmp.append(list())
            self.tile_groups.append(tmp)
        
        # Assign tiles to groups
        for i in range(self.dimension):
            for j in range(self.dimension):
                row_index = i // group_rows
                col_index = j // group_cols
                group = self.tile_groups[row_index][col_index]
                group.append(self.tiles[i][j])
        
        # Assign starting possibilities
        for i in range(self.dimension):
            for j in range(self.dimension):
                tile = self.tiles[i][j]
                tile.possibilities = list(range(1, self.dimension + 1))
    
    def __str__(self):
        longest_number = len(str(self.dimension))

        def group_separator():
            string = ""
            for i in range(self.group_rows):
                string += "++"
                for j in range(self.group_cols * (2 + longest_number) + self.group_rows - 1):
                    string += "-"
            string += "++\n"
            string *= 2
            return string
        
        def row_separator():
            string = ""
            for i in range(self.group_rows):
                for j in range(self.group_cols * (2 + longest_number) + self.group_rows - 1 + 2):
                    string += "-"
            string += "--\n"
            return string
        
        def row_string(row):
            string = ""
            for i in range(len(row)):
                if i % self.group_cols == 0:
                    string += "||"
                else:
                    string += "|"
                string += " "

                number = row[i].number
                number_len = len(str(number))
                if number == 0:
                    number_len = 0
                for i in range(longest_number - number_len):
                    string += " "
                if number != 0:
                    string += str(number)

                string += " "
            string += "||\n"
            return string

        s = ""

        for i in range(self.dimension):
            if i % self.group_rows == 0:
                s += group_separator()
            else:
                s += row_separator()
            s += row_string(self.tiles[i])
        s += group_separator()

        return s
    
    def get_group(self, row, col):
        row_index = row // self.group_rows
        col_index = col // self.group_cols
        return self.tile_groups[row_index][col_index]
    
    def remove_possibilities(self, row, col):
        tile = self.tiles[row][col]

        if tile.number == 0:
            return

        # Remove possibilities from row
        for i in range(self.dimension):
            t = self.tiles[row][i]
            if tile.number in t.possibilities:
                t.possibilities.remove(tile.number)
        
        # Remove possibilities from column
        for i in range(self.dimension):
            t = self.tiles[i][col]
            if tile.number in t.possibilities:
                t.possibilities.remove(tile.number)
        
        # Remove possibilities from group
        group = self.get_group(row, col)
        for t in group:
            if tile.number in t.possibilities:
                t.possibilities.remove(tile.number)
        
        tile.possibilities = list()

    def set_tile(self, number, row, col):
        tile = self.tiles[row][col]
        tile.number = number
        self.remove_possibilities(row, col)

    def copy(self):
        b = Board(self.group_rows, self.group_cols)

        for i in range(self.dimension):
            for j in range(self.dimension):
                old_tile = self.tiles[i][j]
                new_tile = b.tiles[i][j]
                new_tile.number = old_tile.number
                for k in range(len(old_tile.possibilities)):
                    new_tile.possibilities.append(old_tile.possibilities[k])
        
        return b
