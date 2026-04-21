import socket
import threading

clients = []
lock = threading.Lock()


def send_to_all(message, sender=None):
    with lock:
        for client in clients[:]:
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    clients.remove(client)
                    client.close()


def handle_client(client_socket, client_addr):
    print(f"Подключился клиент {client_addr}")

    try:
        client_socket.send("Добро пожаловать в чат!".encode('utf-8'))
    except:
        client_socket.close()
        return

    send_to_all(f"Клиент {client_addr} вошёл в чат", client_socket)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            text = message.decode('utf-8')
            print(f"{client_addr}: {text}")
            send_to_all(f"{client_addr}: {text}", client_socket)
        except:
            break

    with lock:
        if client_socket in clients:
            clients.remove(client_socket)

    client_socket.close()
    print(f"Клиент {client_addr} отключился")
    send_to_all(f"Клиент {client_addr} покинул чат")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen()

print('Сервер запущен и ждёт клиентов...')

while True:
    client_socket, client_addr = server_socket.accept()
    with lock:
        clients.append(client_socket)

    thread = threading.Thread(target=handle_client, args=(client_socket, client_addr), daemon=True)
    thread.start()
