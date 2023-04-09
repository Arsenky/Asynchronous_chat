# -*- coding: UTF-8 -*-

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
import time
import json

def send_presence_massage(clt_soc):
        connection_massage = { "action":"presence", "time": time.time(), "type":"status", "user": { "account_name":"C0deMaver1ck", "status":"Yep, I am here!" } }
        clt_soc.send((json.dumps(connection_massage)).encode('utf-8'))


def main(ip_addr, ip_port):
    
    clt_connect = (str(ip_addr), int(ip_port))
    print(f'Клиент стартовал {clt_connect}')

    clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

    # посылаем запрос на соединение
    clt_soc.connect((str(ip_addr), int(ip_port)))

    send_presence_massage(clt_soc)

    print(json.loads(clt_soc.recv(256).decode('utf-8')))

    print('Клиент закончен')


if __name__ == '__main__':
    #    try:
    if len(argv) > 1:
        mip_addr = argv[1]
        # print('ipa = ', mip_addr)
        if len(argv) > 2:
            mip_port = int(argv[2])
            # print('ipp = ', mip_port)
            
        else:
            mip_port = 7777
            # print('ipp = ', mip_port)

        main(mip_addr, mip_port)
    else:
        print('недопустимые параметры >>>python client.py <addr> [<port>]')
        exit(1)

#    except Exception as e:
#        print(e)
