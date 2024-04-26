from socket import *
import sys,os
import time
import threading

def create_server_soc(port):
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind(('', port))
    serv_sock.listen()
    return serv_sock


def run_server(port=55555):
    print(f'Start server: {port}')
    serv_sock = create_server_soc(port)
    
    cid = 0

    while True:
        cli_sock = accept_client_conn(serv_sock, cid)
        t = threading.Thread( target=serve_cli,
                             args=(cli_sock, cid))
        t.start()
        cid += 1


def accept_client_conn(serv_sock, cid):
    cli_sock, cli_addr = serv_sock.accept()
    print(f'client #{cid} connected:'
          f'{cli_addr[0]}:{cli_addr[1]}')
    return cli_sock


def serve_cli(cli_sock, cid):
    request = read_request(cli_sock)
    if request is None:
        print(f'client #{cid} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(cli_sock, response, cid)


def read_request(cli_sock, delimeter = b'!'):
    request = bytearray()
    try:
        while True:
            chuck = cli_sock.recv(4)
            if not chuck:
                return None
            request += chuck
            if delimeter in request:
                return request
    except ConnectionResetError as e:
        return None
    except:
        raise


def handle_request(request):
    print(f'start handled')
    time.sleep(5)
    return request[::-1]


def write_response(cli_sock, response, cid):
    cli_sock.sendall(response)
    cli_sock.close()
    print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))
