import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print('Сервер отключился')
                break
            print(message.decode('utf-8'))
        except:
            print('Соединение потеряно')
            break

    client_socket.close()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
thread.start()

while True:
    try:
        text = input()
        if text.lower() == 'exit':
            break
        client_socket.send(text.encode('utf-8'))
    except:
        break

client_socket.close()
print('Клиент завершил работу')
