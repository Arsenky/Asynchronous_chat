# -*- coding: UTF-8 -*-

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import time
import json


def receive_massage(client):
    raw_massage = client.recv(256)
    massage = json.loads(raw_massage.decode('utf-8'))
    print('Получили сообщение от клиента')
    return massage

def send_presence_answer(client):
    client.send(
                (json.dumps({"response": 200, "alert": "Успешное подключение"})).encode('utf-8')
                )
    print('Отправили ответ')

def process_massage(client, massage):

    action = massage['action']

    if action == 'presence':
        send_presence_answer(client)
    elif action == 'quit':
        client.send((json.dumps({"response": "200", "alert": "Отключаюсь"})).encode('utf-8'))
        print('Получен сигнал на отключение')
        print('сеанс закрыт, сервер остановлен')
        exit(1)

def main(ip_addr, ip_port):
    print('MY Server RUN ^^^ ', end='')

    srv_connect = (str(ip_addr), int(ip_port))
    print(srv_connect)
    srv_soc = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM - TCP
    srv_soc.bind((ip_addr, ip_port))  # ( aдрес, порт )
    print()
    srv_soc.listen(5)  # одновременно обслуживает не более 5 запросов

    while True:
        client, addr = srv_soc.accept()
        print('--------------\nожидание приёма ')
        print('получаем запрос на соединение от ', addr)

        massage = receive_massage(client)

        process_massage(client, massage)

        

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
        mip_addr =''
    main(mip_addr, mip_port)


       

#    except Exception as e:
#        print(e)