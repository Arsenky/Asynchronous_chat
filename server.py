# -*- coding: UTF-8 -*-

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import time
import json
import logging
import log.server_log_config
import log.server_log_config
from log.log_decorator import log
import select

server_logger = logging.getLogger('server')


@log
def receive_massage(client: socket) -> dict:
    raw_massage = client.recv(256)
    massage = json.loads(raw_massage.decode('utf-8'))
    server_logger.info(f'Получили сообщение от клиента: {massage}')
    return massage


@log
def send_presence_answer(client: socket):
    client.send(
        (json.dumps({"response": 200, "alert": "Успешное подключение"})).encode(
            'utf-8')
    )
    server_logger.info('Отправили ответ')


@log
def process_massage(client: socket, massage: dict):

    action = massage['action']

    if action == 'presence':
        send_presence_answer(client)
    elif action == 'quit':
        client.send(
            (json.dumps({"response": "200", "alert": "Отключаюсь"})).encode('utf-8'))
        server_logger.warning(
            'Получен сигнал на отключение, сеанс закрыт, сервер остановлен')
        exit(0)


def read_massage(r_clients, all_clients) -> dict:
    data = None
    for sock in r_clients:
        data = json.loads(sock.recv(1024).decode('utf-8'))
        action = data['action']
        if action == 'quit':
            all_clients.remove(sock)   
            print(f'Клиент {sock.getpeername()} отключился')
            data = {}
        elif action == 'massage':
            pass
        elif action == 'stop':
            print('Получен сигнал на отключение сервера')
            server_logger.warning('Получен сигнал на отключение сервера')
            data = {'action' : 'stop'}
            exit(0)
    return data

def resend_massage(massage, w_clients, all_clients):
    for sock in w_clients:
        sock.send(json.dumps(massage).encode('utf-8'))
    
def main(ip_addr: str, ip_port: int):
    print('MY Server RUN ^^^ ', end='')

    clients = []

    srv_connect = (str(ip_addr), int(ip_port))
    print(srv_connect)
    srv_soc = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM - TCP
    srv_soc.bind((ip_addr, ip_port))  # ( aдрес, порт )
    srv_soc.listen(5)  # одновременно обслуживает не более 5 запросов
    srv_soc.settimeout(0.5)
    srv_soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # для быстрого автовысвобождения порта

    while True:
        try:
            conn, addr = srv_soc.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
           
        finally:
            # Проверить наличие событий ввода-вывода
            massage = None
            wait = 3
            r = []
            w = []
            r, w, e = select.select(clients, clients, [], wait)

            # отладочные выводы
            print('передающие сокеты:')
            for sock in r:
                print(sock.getpeername())
            print('принимающие сокеты:')
            for sock in w:
                print(sock.getpeername())
            print()

            if r:  
                massage = read_massage(r, clients)  
                print(massage)

            # удаляем отправителей из списка получателей
            for sock in r:
                w.remove(sock)

            if massage:
                resend_massage(massage, w, clients)
            
            time.sleep(3)

if __name__ == '__main__':
    if '-p' in argv:
        mip_port = int(argv[argv.index('-p')+1])
        if mip_port < 1024 or mip_port > 65535:
            print('порт должен быть в диапазоне от 1024 до 65535')
            exit(1)
    else:
        mip_port = 7777

    if '-a' in argv:
        mip_addr = argv[argv.index('-a')+1]
    else:
        mip_addr = ''
    main(mip_addr, mip_port)


