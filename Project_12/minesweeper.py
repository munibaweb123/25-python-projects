import random
import re
# let's create a board object to represent the minesweeper game
# This is so that we can just say "create a new board object", or
# "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        # let's keep track of these parameters, they'll be helpful
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        # let's create the board
        # helper function!
        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()
        # initialize a set to keep track of which location
        # we'll save (row, col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer)
        # but since we have a 2-D board, list of lists is most natural)
        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this creates an array like this:
        # [[None, None, ..., None]],
        # [None, None, ...., None],
        # [...                   ],
        # [None, None, ..., None]]
        # we can see how this represents a board!
        # plant the bombs
        bomb_planted = 0
        while bomb_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1)# return random integer N such that a <= N <= b
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue
            board[row][col] = '*'
            bomb_planted += 1

        return board
    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all empty spaces
        # represents how many neighboring bombs there are. we can precompute these and it'll say
        # effort checking what's arround the board later on :)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self, row, col):
            # let's iterate through each of the neighboring position and sum number of bombs
            # top-left(row-1,col-1)
            # top-middle(row-1,col)
            # top right: (row-1, col+1)
            # left: (row, col-1)
            # right: (row, col+1)
            # bottom left: (row+1, col -1)
            # bottom middle: (row+1, col)
            # bottom right: (row+1,col+1)

            # make sure to not go out of bombs!

        num_neighboring_bombs = 0
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1), min(self.dim_size-1,col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs
    def dig(self, row, col):
        # dig at that location:
        # return True if successful dig, false if bomb dug
        # a few scenarios:
        # hit a bomb -> game over
        # dig at location with neighboring bomb -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbors!
        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        # Check if the cell is empty and recursively dig neighbors
        if self.board[row][col] == 0:
            for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
                for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                    if (r, c) in self.dug:
                        continue
                    self.dig(r, c)  # Correctly call the dig method
        return True
    
    def __str__(self):
        # this is a magic function if you call print on this object,
        # it will print out what this function returns
        # return a string that shows the board to the player
        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # Add this line to return the string representation of the board
        return "\n".join([" ".join(row) for row in visible_board])  # Return the visible board as a string

def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    first_move = True  # Track if it's the first move
    safe = True

    while len(board.dug) < board.dim_size * board.dim_size - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input('Where would you like to dig? Input as row,col:'))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print('Invalid location, Try again')
            continue

        # If it's the first move, check if the cell is a bomb
        if first_move and board.board[row][col] == '*':
            print("You dug a bomb! Let's try again.")
            continue  # Skip this move and ask for input again

        # if it's valid we dig
        safe = board.dig(row, col)
        first_move = False  # Set first_move to False after the first valid move

        if not safe:
            # dug a bomb ahhhh
            break

    # 2 ways to end loop, let's check which one
    if safe:
        print('Congratulations!!! You are Victorious')
        # let's reveal the whole board!
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
    else:
        print('sorry!, game over')
if __name__ == '__main__':
    play()