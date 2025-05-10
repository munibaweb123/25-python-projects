import pygame
import socket
import pickle
import chess
import threading
# Initialize Pygame Mixer
pygame.mixer.init()

# Load Sounds
move_sound = pygame.mixer.Sound("move.mp3")
capture_sound = pygame.mixer.Sound("capture.mp3")
check_sound = pygame.mixer.Sound("check.mp3")

# Constants
WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Chess")

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

# Receive initial board state and player ID
fen, player_id = pickle.loads(client.recv(1024))
board = chess.Board(fen)

# Draw the chessboard
def draw_board(win, selected_square=None, legal_moves=[]):
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            if board.is_check() and square == board.king(board.turn):
                color = (255, 0, 0)  # Red for the king in check
            elif selected_square is not None and selected_square == square:
                color = (255, 255, 0)  # Yellow for the selected square
            elif square in legal_moves:
                color = (0, 255, 0)  # Green for legal moves
            else:
                color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
# Draw the chess pieces
def draw_pieces(win, board):
    font = pygame.font.SysFont("dejavusans", 48)
    piece_symbols = {
        "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
        "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece_symbols[str(piece)]
            row = 7 - square // 8
            col = square % 8
            text = font.render(symbol, True, (0, 0, 0))
            x = col * SQ_SIZE + SQ_SIZE // 4
            y = row * SQ_SIZE + SQ_SIZE // 6
            win.blit(text, (x, y))

# Get the square clicked by the user
def get_square(pos):
    x, y = pos
    col = x // SQ_SIZE
    row = 7 - (y // SQ_SIZE)
    return chess.square(col, row)

# Thread to receive updates from the server
def receive_thread():
    global board
    while True:
        try:
            data = pickle.loads(client.recv(1024))
            print("Received FEN:", data[0])  # Debug: Print the FEN string
            board.set_fen(data[0])
        except Exception as e:
            print("Error in receive_thread:", e)
            break

# Start the receive thread
threading.Thread(target=receive_thread, daemon=True).start()

# Main game loop
selected_square = None
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    legal_moves = []
    if selected_square is not None:
        legal_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
    draw_board(win, selected_square, legal_moves)  # Pass legal moves to highlight them
    draw_pieces(win, board)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and board.turn == (player_id == 0):
            square = get_square(pygame.mouse.get_pos())
            if selected_square is None:
                # Select the square if it contains a piece of the current player
                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected_square = square
            else:
                # Attempt to make a move
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    # Play capture sound if the destination square has an opponent's piece
                    if board.piece_at(square):
                        capture_sound.play()
                    else:
                        move_sound.play()

                    # Handle check sound
                    if board.gives_check(move):
                        check_sound.play()

                    print("Sending move:", move.uci())  # Debug: Print the move being sent
                    client.send(move.uci().encode())
                selected_square = None  # Deselect the square after making a move

pygame.quit()