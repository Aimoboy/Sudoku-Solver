class SolutionData:
    def __init__(self, solved, board, time, backtracks):
        self.solved = solved
        self.board = board
        self.time = time
        self.backtracks = backtracks
    
    def print_report(self):
        if self.solved:
            print("The board was solved in {0} seconds with {1} backtracks.".format(self.time, self.backtracks))
        else:
            print("The board was not solved.")
