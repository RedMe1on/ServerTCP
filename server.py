import socket

serv_socket = socket.socket(socket.AF_INET,  # выбор семейство протоколов - для сетевого протокола IPv4
                            socket.SOCK_STREAM,  # выбор свойства сокета - потоковый
                            socket.IPPROTO_TCP)  # выбор протокола

serv_socket.bind(('127.0.0.1', 53210))

serv_socket.listen(2)  # 2 - размер очереди входящих подключений (backlog)
print(serv_socket)

while True:

    client_sock, client_addr = serv_socket.accept()  # Получаем соединение из backlog
    print(f'Connected by {client_addr}')
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(data)
    client_sock.close()



