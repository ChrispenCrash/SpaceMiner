import socket
import threading
import pickle
import random
import os
import sys
import signal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import GAME_WIDTH, GAME_HEIGHT, ASTEROID_COUNT
from asteroid import Asteroid

class GameServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.game_state = {
            'players': {},
            'asteroids': [Asteroid().serialize() for _ in range(ASTEROID_COUNT)]
        }
        self.running = True

    def handle_client(self, client_socket, client_address):
        print(f"New connection: {client_address}")
        self.clients.append(client_socket)
        player_id = len(self.clients)
        self.game_state['players'][player_id] = {'pos': (GAME_WIDTH // 2, GAME_HEIGHT // 2), 'score': 0}

        # Send initial game state to the new client
        try:
            initial_data = pickle.dumps(self.game_state)
            client_socket.sendall(initial_data)
            print(f"Sent initial game state to player {player_id}")
        except Exception as e:
            print(f"Error sending initial game state to player {player_id}: {e}")

        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                action = pickle.loads(data)
                print(f"Received action from player {player_id}: {action}")
                self.process_action(player_id, action)
                self.broadcast_game_state()
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                break

        print(f"Connection closed: {client_address}")
        self.clients.remove(client_socket)
        del self.game_state['players'][player_id]
        client_socket.close()

    def process_action(self, player_id, action):
        if action['type'] == 'move':
            self.game_state['players'][player_id]['pos'] = action['pos']
        elif action['type'] == 'score':
            self.game_state['players'][player_id]['score'] += action['score']

    def broadcast_game_state(self):
        data = pickle.dumps(self.game_state)
        for client in self.clients:
            try:
                client.sendall(data)
            except Exception as e:
                print(f"Error sending data to client: {e}")

    def run(self):
        print("Server started")
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except Exception as e:
                print(f"Error accepting connections: {e}")

    def shutdown(self):
        print("Shutting down server...")
        self.running = False
        self.server.close()
        for client in self.clients:
            client.close()

def signal_handler(sig, frame):
    print("Signal received, shutting down server...")
    server.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    server = GameServer()

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Start the server in the main thread
    server.run()