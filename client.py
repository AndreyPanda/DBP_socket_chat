import socket
from threading import Thread
from datetime import datetime


HOST = "127.0.0.1"
PORT = 12345
separator_token = "<SEP>"

s = socket.socket()
print(f"[*] Connecting to {HOST}:{PORT}...")
s.connect((HOST, PORT))
print("[+] Connected.")
name = input("Enter your name: ")


def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()
            print("\n" + message)
        except ConnectionResetError:
            print(f"[!] Error: The server has disconnected!")
            break


t = Thread(target=listen_for_messages)
t.daemon = True
t.start()


def send_messages():
    while True:
        to_send = input()
        if to_send.lower() == "q":
            print(f"You leave the room\n")
            break
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        to_send = f"[{date_now}] {name}{separator_token}{to_send}"
        s.send(to_send.encode())


send_messages()
s.close()
