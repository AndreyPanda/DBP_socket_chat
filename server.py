import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345
separator_token = "<SEP>"

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
print(f"[*] Listening at {HOST}:{PORT}")


def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except ConnectionResetError:
            print(f"[!] Client {client_address} has left the room.")
            client_sockets.remove(cs)
            break
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            if client_socket != cs:
                client_socket.send(msg.encode())


while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()
s.close()
