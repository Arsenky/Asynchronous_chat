# -*- coding: UTF-8 -*-

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
import time
import json
import logging
import log.client_log_config, log.server_log_config
from log.log_decorator import log


client_logger = logging.getLogger('client')

@log
def create_massage(user_massage : str) -> dict:
        massage = { "action" : "massage", "time" : time.time(), "user_massage" : user_massage}
        client_logger.info(f'Сформированно сообщение серверу: {massage}')
        return massage

@log     
def send_massage(clt_soc : socket, user_massage):
    massage = create_massage(user_massage)
    clt_soc.send((json.dumps(massage)).encode('utf-8'))
    client_logger.info('Сообщение отправленно серверу')


def main(ip_addr : str, ip_port : int):
    while True:
        try:
            clt_connect = (ip_addr, ip_port)
            client_logger.info(f'Клиент стартовал {clt_connect}')

            clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

            # посылаем запрос на соединение
            clt_soc.connect((str(ip_addr), int(ip_port)))
            break
        except:
            print('Сервер недоступен')
            time.sleep(1)

    while True:
        massage = input(f'Введите сообщение остальным клиентам от {clt_soc.fileno()}, {clt_soc.getpeername()}: ')
        send_massage(clt_soc, massage)
        print('Сообщение отправленно\n')

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

