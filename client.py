import socket
import threading
from cryptography.fernet import Fernet

# Paste the same key that was printed by the server
key = input("Enter encryption key from server: ").encode()
cipher = Fernet(key)

# Setup TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))
print("Connected to server!")

# Function to receive messages
def receive():
    while True:
        encrypted_msg = client.recv(1024)
        if not encrypted_msg:
            break
        msg = cipher.decrypt(encrypted_msg).decode()
        print(f"\nServer: {msg}")

# Start receiving in background
threading.Thread(target=receive, daemon=True).start()

# Function to send messages
while True:
    message = input("You: ")
    encrypted_msg = cipher.encrypt(message.encode())
    client.send(encrypted_msg)
