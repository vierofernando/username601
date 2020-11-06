class TicTacToe:
    def __init__(self, player: str = "O", opponent: str = "X", default: str = "-"):
        self.board = [default] * 9 # build the board
        self.winning_moves = [[int(a) for a in list(i)] for i in "012,345,678,048,642".split(",")] # list of winning moves
        self.filled = [] # array of used indexes
        self.player, self.opponent, self.default = player, opponent, default # symbols
        self.is_on_range = (lambda x: int(x) in range(1,10)) # method to check if is on board range
        self.current_turn = player # set the current turn to the player

    def check_if_win(self):
        if len(self.filled) == len(self.board): return "?" # draw
        for x, y, z in self.winning_moves:
            if (self.board[x] == self.board[y] == self.board[z]) and (self.board[x] != self.default):
                return self.board[x] # this character wins
        return None # no one wins yet

    def add_move(self, order: int, opponent: bool):
        if (order in self.filled) or (not self.is_on_range(order)): return None # check if is number and is valid
        self.filled.append(order) # add to used array, so the column can't be used anymore
        self.board[order - 1] = self.opponent if opponent else self.player # change the display in board
        self.current_turn = self.player if opponent else self.opponent # change the current player
        return 1

    def show(self): # self-explanatory.
        string = ""
        for column in range(len(self.board)):
            if column % 3 == 0: string += "\n"
            string += self.board[column] + " "
        return string + "\n"