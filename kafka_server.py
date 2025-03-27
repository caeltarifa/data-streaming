import socket
import json
import threading
import signal
import sys
from pathlib import Path
#from utils import setup_logging, log_message # uncomment when you have utils.py

#logger = setup_logging() # uncomment when you have utils.py


class KafkaServer:

    def __init__(self, host='0.0.0.0', port=9292):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.messages = []
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        #log_message(logger, "info", f"Kafka server started on {self.host}:{self.port}") # uncomment when you have utils.py
        print(f"Kafka server started on {self.host}:{self.port}")

        def signal_handler(sig, frame):
            print("Shutting down server...")
            self.running = False
            self.socket.close()
            for client in self.clients:
                client.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while self.running:
            try:
                client, address = self.socket.accept()
                self.clients.append(client)
                client_thread = threading.Thread(target=self.handle_client,
                                                 args=(client, address))
                client_thread.start()
            except OSError:
                if self.running:
                    raise  #re-raise if it was a different error.

    def handle_client(self, client, address):
        while self.running:
            try:
                data = client.recv(1024)
                if not data:
                    break

                message = json.loads(data.decode())
                with self.lock:
                    self.messages.append(message)
                    for c in self.clients:
                        if c != client:  # Don't send back to producer
                            try:
                                c.send(json.dumps(message).encode())
                            except (socket.error, ConnectionResetError) as e:
                                #log_message(logger, "error", f"Error sending to client {address}: {str(e)}") # uncomment when you have utils.py
                                print(
                                    f"Error sending to client {address}: {str(e)}"
                                )
                                self.clients.remove(c)

            except (socket.error, ConnectionResetError) as e:
                #log_message(logger, "error", f"Error handling client {address}: {str(e)}") # uncomment when you have utils.py
                print(f"Error handling client {address}: {str(e)}")
                break
            except json.JSONDecodeError as e:
                #log_message(logger, "error", f"JSON decode error from {address}: {str(e)}") # uncomment when you have utils.py
                print(f"JSON decode error from {address}: {str(e)}")
                break
            except Exception as e:
                #log_message(logger, "error", f"Unexpected error from {address}: {str(e)}") # uncomment when you have utils.py
                print(f"Unexpected error from {address}: {str(e)}")
                break

        client.close()
        if client in self.clients:
            self.clients.remove(client)


if __name__ == "__main__":
    server = KafkaServer()
    server.start()
