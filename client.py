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
def create_presence_massage():
        connection_massage = { "action":"presence", "time": time.time(),
            "type":"status", "user": { "account_name":"C0deMaver1ck", "status":"Yep, I am here!" } 
            }
        client_logger.info(f'Сформированно сообщение серверу: {connection_massage}')
        return connection_massage

@log     
def send_presence_massage(clt_soc : socket):
    massage = create_presence_massage()
    clt_soc.send((json.dumps(massage)).encode('utf-8'))
    client_logger.info('Сообщение отправленно серверу')

@log
def receive_answer(clt_soc : socket) -> dict:
    massage = json.loads(clt_soc.recv(256).decode('utf-8'))
    client_logger.info(f'Ответ от серевера: {massage["response"]}, {massage["alert"]}')
    return massage

# функция отправки сигнала на остановку сервера
@log
def send_quit_signal(clt_soc : socket):
    signal = { "action":"quit", "time": time.time()}
    clt_soc.send((json.dumps(signal)).encode('utf-8'))
    massage = json.loads(clt_soc.recv(256).decode('utf-8'))
    if massage["alert"] == 'Отключаюсь':
        client_logger.warning('Сервер отключился')

def main(ip_addr : str, ip_port : int):

    clt_connect = (ip_addr, ip_port)
    client_logger.info(f'Клиент стартовал {clt_connect}')

    clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

    # посылаем запрос на соединение
    clt_soc.connect((str(ip_addr), int(ip_port)))

    send_presence_massage(clt_soc)
    
    receive_answer(clt_soc)

    clt_soc.close()
    clt_soc = socket(AF_INET, SOCK_STREAM)
    clt_soc.connect((str(ip_addr), int(ip_port)))

    # send_quit_signal(clt_soc)


    client_logger.info('Сеанс закончен')
    n = input('ожидаю')



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
