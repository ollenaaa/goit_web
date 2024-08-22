import socket
from datetime import datetime
import json

UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            current_datetime = datetime.now()
            data_dict = {current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"): {key: value for key, value in [el.split("=") for el in data.decode().split("&")]}}

            dictObj = {}

            with open('../../storage/data.json', 'r') as fp:
                dictObj = json.load(fp)

            dictObj[current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")] = {key: value for key, value in [el.split("=") for el in data.decode().split("&")]}

            with open('../../storage/data.json', "w") as fh:
                json.dump(dictObj, fh, indent = 4, separators=(',', ': '))

            print(f'Received data: {data_dict} from: {address}')
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


if __name__ == "__main__":
    run_server(UDP_IP, UDP_PORT)