import socket
import threading
import pickle
import chess

# Server setup
server = "127.0.0.1"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(2)

print("Server started. Waiting for connections...")

# Initialize the chessboard
board = chess.Board()
clients = []

# Handle client connections
def client_thread(conn, player_id):
    global board
    conn.send(pickle.dumps((board.fen(), player_id)))

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            move = chess.Move.from_uci(data)
            if move in board.legal_moves:
                board.push(move)
                broadcast(board.fen())
        except:
            break

    conn.close()
    clients.remove(conn)
    print(f"Player {player_id} disconnected.")

# Broadcast the board state to all clients
def broadcast(fen):
    print("Broadcasting FEN:", fen)  # Debug
    for client in clients:
        try:
            client.send(pickle.dumps((fen,)))
        except:
            clients.remove(client)

# Accept connections
player_id = 0
while True:
    conn, addr = s.accept()
    print(f"Player {player_id} connected from {addr}.")
    clients.append(conn)
    threading.Thread(target=client_thread, args=(conn, player_id)).start()
    player_id += 1