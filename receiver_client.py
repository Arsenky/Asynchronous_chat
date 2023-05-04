# -*- coding: UTF-8 -*-

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
import time
import json
import logging
import log.client_log_config, log.server_log_config
from log.log_decorator import log


client_logger = logging.getLogger('client')

# @log
def receive_massage(clt_soc : socket) -> dict:
    massage = json.loads(clt_soc.recv(256).decode('utf-8'))
    client_logger.info(f'Принято ообщение с серевера: {massage}')
    return massage


def main(ip_addr : str, ip_port : int):

    clt_connect = (ip_addr, ip_port)
    client_logger.info(f'Клиент стартовал {clt_connect}')

    clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

    # посылаем запрос на соединение
    clt_soc.connect((str(ip_addr), int(ip_port)))

    while True:
        try:
            massage = receive_massage(clt_soc)
        except:
            pass
        else:
            print(f"Полученно сообщение от другого клиента: {massage['user_massage']}\n")
            if massage['user_massage'] == 'Exit':
                clt_soc.close()
                print('Сеанс завершен')

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
