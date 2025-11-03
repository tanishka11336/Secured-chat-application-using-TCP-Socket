import socket
import threading
from cryptography.fernet import Fernet

# Generate or use a fixed key for both client and server
key = Fernet.generate_key()
cipher = Fernet(key)

print(f"Encryption Key (share this with client): {key.decode()}")

# Setup TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(1)
print("Server is waiting for connection...")

conn, addr = server.accept()
print(f"Connected to {addr}")

# Function to receive messages
def receive():
    while True:
        encrypted_msg = conn.recv(1024)
        if not encrypted_msg:
            break
        msg = cipher.decrypt(encrypted_msg).decode()
        print(f"\nClient: {msg}")

# Start receiving in background
threading.Thread(target=receive, daemon=True).start()

# Function to send messages
while True:
    message = input("You: ")
    encrypted_msg = cipher.encrypt(message.encode())
    conn.send(encrypted_msg)
