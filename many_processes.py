from socket import *
import sys,os
import time


def create_server_soc(port):
    serv_sock = socket(AF_INET, SOCK_STREAM)
    serv_sock.bind(('', port))
    serv_sock.listen()
    return serv_sock


def run_server(port=55555):
    print(f'Start server: {port}')
    serv_sock = create_server_soc(port)
    active_children = set()
    cid = 0

    while True:
        cli_sock = accept_client_conn(serv_sock, cid)
        child_pid = serve_cli(cli_sock, cid)
        active_children.add(child_pid)
        reap_children(active_children)
        cid += 1


def accept_client_conn(serv_sock, cid):
    cli_sock, cli_addr = serv_sock.accept()
    print(f'client #{cid} conneected:'
          f'{cli_addr[0]}:{cli_addr[1]}')
    return cli_sock


def serve_cli(cli_sock, cid):
    child_pid = os.fork()
    if child_pid:
        # Родительский процесс, не делаем ничего
        cli_sock.close()
        return child_pid
    request = read_request(cli_sock)
    if request is None:
        print(f'client #{cid} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(cli_sock, response, cid)
    os._exit(0)


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
    time.sleep(5)
    return request[::-1]


def write_response(cli_sock, response, cid):
    cli_sock.sendall(response)
    cli_sock.close()
    print(f'Client #{cid} has been served')

def reap_children(active_children):
  for child_pid in active_children.copy():
    child_pid, _ = os.waitpid(child_pid, os.WNOHANG)
    if child_pid:
      active_children.discard(child_pid)




if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))
