# -*- coding: UTF-8 -*-

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import time
import json
import logging
import log.client_log_config, log.server_log_config
from log.log_decorator import log
import threading

client_logger = logging.getLogger('client')

@log
def console(clt_soc):
    while True:
        command = input('Введите команду: ')
        if command == 'massage':
            send_massage(clt_soc)
        elif command == 'exit':
            send_quit_signal(clt_soc)
            clt_soc.close()
            print('Работа клиента завершена')
            client_logger.info('Работа клиента завершена')
            exit(0)
        elif command == 'stop':
            send_stop_signal(clt_soc)
            print('Послан сигнал на отключение сервера')
            client_logger.info('Послан сигнал на отключение сервера')
        else:
            print('Неизвестная команда')

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
def receive_massage(clt_soc : socket):
    while True:
        massage = json.loads(clt_soc.recv(256).decode('utf-8'))
        # client_logger.info(f'Ответ от серевера: {massage["response"]}, {massage["alert"]}')
        print(f"\nПринято сообщение : {massage['user_massage']}")
        time.sleep(1)

# функция отправки сигнала серверу об отключении клиента
@log
def send_quit_signal(clt_soc : socket):
    signal = { "action": "quit", "time": time.time()}
    clt_soc.send((json.dumps(signal)).encode('utf-8'))

# функция отправки сигнала на остановку сервера
@log
def send_stop_signal(clt_soc : socket):
    signal = { "action": "stop", "time": time.time()}
    clt_soc.send((json.dumps(signal)).encode('utf-8'))



@log
def create_massage() -> dict:
        user_massage = input('Введите сообщение: ')
        massage = { "action" : "massage", "time" : time.time(), "user_massage" : user_massage}
        client_logger.info(f'Сформированно сообщение серверу: {massage}')
        return massage

@log     
def send_massage(clt_soc : socket):
        massage = create_massage()
        clt_soc.send((json.dumps(massage)).encode('utf-8'))
        client_logger.info('Сообщение отправленно серверу')


def main(ip_addr : str, ip_port : int):
    try:
        clt_connect = (ip_addr, ip_port)
        client_logger.info(f'Клиент стартовал {clt_connect}')

        clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

        # посылаем запрос на соединение
        clt_soc.connect((str(ip_addr), int(ip_port)))
    except:
        print('Сервер недоступен')
        exit(1)


    user_console = threading.Thread(target=console, args=(clt_soc, ))
    user_console.daemon = True
    user_console.start()
    

    receiver = threading.Thread(target=receive_massage, args=(clt_soc, ))
    receiver.daemon = True
    receiver.start()

    user_console.join()



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
