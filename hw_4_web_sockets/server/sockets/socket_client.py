import socket


def run_client(data, UDP_IP = '127.0.0.1', UDP_PORT = 5000):
    print(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = UDP_IP, UDP_PORT
    sock.sendto(data.encode(), server)
    print(f'Send data: {data} to server: {server}')
    sock.close()