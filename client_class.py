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

class Client():

    def __init__(self, ip_addr, ip_port) -> None:
        self.ip_addr = ip_addr
        self.ip_port = ip_port

    @log
    def console(self):
        while True:
            command = input('Введите команду: ')
            if command == 'massage':
                self.send_massage()
            elif command == 'exit':
                self.send_quit_signal()
                self.clt_soc.close()
                print('Работа клиента завершена')
                client_logger.info('Работа клиента завершена')
                exit(0)
            elif command == 'stop':
                self.send_stop_signal()
                print('Послан сигнал на отключение сервера')
                client_logger.info('Послан сигнал на отключение сервера')
            else:
                print('Неизвестная команда')

    @log
    def create_presence_massage(self) -> dict:
            connection_massage = { "action" : "presence", "time": time.time(), "nick_name" : self.nick_name} 
            client_logger.info(f'Сформированно сообщение о присутствии серверу: {connection_massage}')
            return connection_massage

    @log     
    def send_presence_massage(self):
        massage = self.create_presence_massage()
        self.clt_soc.send((json.dumps(massage)).encode('utf-8'))
        client_logger.info('Сообщение о присутствии отправленно серверу')

    @log
    def receive_massage(self):
        while True:
            try:
                massage = json.loads(self.clt_soc.recv(256).decode('utf-8'))
            except:
                print('Сервер недоступен')
                time.sleep(1)
            else:
                print(f"\nПринято сообщение : {massage['user_massage']}")
                

    # функция отправки сигнала серверу об отключении клиента
    @log
    def send_quit_signal(self):
        signal = { "action": "quit", "time": time.time()}
        self.clt_soc.send((json.dumps(signal)).encode('utf-8'))

    # функция отправки сигнала на остановку сервера
    @log
    def send_stop_signal(self):
        signal = { "action": "stop", "time": time.time()}
        self.clt_soc.send((json.dumps(signal)).encode('utf-8'))



    @log
    def create_massage(self) -> dict:
            user_massage = input('Введите сообщение: ')
            reciever = input('Введите никнейп получателя: ')
            massage = { "action" : "massage", "time" : time.time(), "sender": self.nick_name, "reciever" : reciever, "user_massage" : user_massage}
            client_logger.info(f'Сформированно сообщение серверу: {massage}')
            return massage

    @log     
    def send_massage(self):
            massage = self.create_massage()
            self.clt_soc.send((json.dumps(massage)).encode('utf-8'))
            client_logger.info('Сообщение отправленно серверу')


    def start(self):
        self.nick_name = input('Ведите свой никнейм: ')
        try:
            clt_connect = (self.ip_addr, self.ip_port)
            client_logger.info(f'Клиент стартовал {clt_connect}')

            self.clt_soc = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP

            # посылаем запрос на соединение
            self.clt_soc.connect((str(self.ip_addr), int(self.ip_port)))
        except:
            print('Сервер недоступен')
            exit(1)
        else:
            self.send_presence_massage()

        user_console = threading.Thread(target=self.console, args=())
        user_console.daemon = True
        user_console.start()
        

        receiver = threading.Thread(target=self.receive_massage, args=())
        receiver.daemon = True
        receiver.start()

        user_console.join()


if __name__ == '__main__':
    Client1 = Client('localhost', 7777)
    Client1.start()
    # if __name__ == '__main__':
    #     #    try:
    #     if len(argv) > 1:
    #         mip_addr = argv[1]
    #         # print('ipa = ', mip_addr)
    #         if len(argv) > 2:
    #             mip_port = int(argv[2])
    #             # print('ipp = ', mip_port)
                
    #         else:
    #             mip_port = 7777
    #             # print('ipp = ', mip_port)

    #         main(mip_addr, mip_port)
    #     else:
    #         print('недопустимые параметры >>>python client.py <addr> [<port>]')
    #         exit(1)

    #    except Exception as e:
    #        print(e)
