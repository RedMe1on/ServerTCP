import socket
import time
from typing import Union
import threading


def run_server(port=53210) -> None:
    serv_sock = create_serv_sock(port)
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        t = threading.Thread(target=serve_client, args=(client_sock, cid))
        t.start()
        cid += 1


def serve_client(client_sock: socket, cid: int) -> None:
    request = read_request(client_sock)
    if request is None:
        print(f'Client {cid}  unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(client_sock, response, cid)


def create_serv_sock(serv_port: int) -> socket:
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind(('', serv_port))
    serv_sock.listen()
    return serv_sock


def accept_client_conn(serv_sock: socket, cid: int) -> socket:
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock


def read_request(client_sock: socket, delimiter=b'!') -> Union[bytearray, None]:
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(4)
            if not chunk:
                # Отключение преждевременное
                return None
            request += chunk
            if delimiter in request:
                return request
    except ConnectionResetError:
        # Соединение неожиданно разорвано
        return None
    except:
        raise


def handle_request(request: bytearray) -> bytearray:
    time.sleep(5)
    return request[::-1]


def write_response(client_sock: socket, response: bytearray, cid: int) -> None:
    client_sock.sendall(response)
    client_sock.close()
    print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server(53210)
