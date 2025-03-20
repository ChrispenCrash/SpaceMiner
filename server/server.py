import socket
import pickle
import threading
import sys
import os
import signal
from server_settings import ASTEROID_COUNT

from asteroid_server import Asteroid

class GameServer:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(1.0)  # Set a timeout for the accept call
        self.server.bind((host, port))
        self.server.listen()
        print(f"Server started on {host}:{port}")

        self.clients = []
        self.running = True
        
        self.game_state = {
            'players': {},
            'asteroids': [Asteroid().serialize() for _ in range(ASTEROID_COUNT)]
        }

    def handle_client(self, client_socket, client_address):
        print(f"New connection: {client_address}")
        self.clients.append(client_socket)
        player_id = len(self.clients)
        self.game_state['players'][player_id] = {'pos': (0, 0), 'angle': 0}

        try:
            # Send player ID
            client_socket.sendall(pickle.dumps(player_id))

            # Send initial game state to the new client
            client_socket.sendall(pickle.dumps(self.game_state))
        except Exception as e:
            print(f"Error sending initial game state to player {player_id}: {e}")

        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                action = pickle.loads(data)
                if action['type'] == 'move':
                    self.game_state['players'][player_id]['pos'] = action['pos']

                self.broadcast_game_state()
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                break

        print(f"Connection closed: {client_address}")
        self.clients.remove(client_socket)
        del self.game_state['players'][player_id]
        client_socket.close()

    def broadcast_game_state(self):
        serialized_state = pickle.dumps(self.game_state)
        disconnected_clients = []
        for client in self.clients:
            try:
                client.sendall(serialized_state)
            except Exception as e:
                print(f"Error sending data to client: {e}")
                disconnected_clients.append(client)

        # Remove disconnected clients
        for client in disconnected_clients:
            self.clients.remove(client)

    def run(self):
        self.game_state = {
            'players': {},
            'asteroids': [Asteroid().serialize() for _ in range(ASTEROID_COUNT)]
        }
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Server error: {e}")

    def shutdown(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.server.close()

if __name__ == "__main__":
    server = GameServer()

    def signal_handler(sig, frame):
        print("Shutting down server...")
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    server.run()