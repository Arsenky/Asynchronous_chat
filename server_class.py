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
from metaclasses import ServerVerifier
from server_database import ServerDataBase

server_logger = logging.getLogger('server')

class Port:

    def __set__(self, instance, value):
        if 65000 < value or value < 0:
            raise TypeError('Некорректный порт')

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name



class Server(metaclass = ServerVerifier):
    ip_port = Port()

    def __init__(self, ip_addr, ip_port):
        self.ip_addr = ip_addr
        self.ip_port = ip_port


    def read_massages(self) -> list:
        data = []
        for sock in self.r:
            massage = json.loads(sock.recv(1024).decode('utf-8'))
            action = massage['action']
            if action == 'quit':
                self.clients.pop(sock)   
                print(f'Клиент {sock.getpeername()} отключился')
            elif action == 'massage':
                data.append(massage)
            elif action == 'stop':
                print('Получен сигнал на отключение сервера')
                server_logger.warning('Получен сигнал на отключение сервера')
                exit(0)
            elif action == 'get_contacts':
                data.append(self.get_contacts(massage))
            elif action == 'add_contact':
                self.db.add_contact(massage['user_login'], massage['login_for_add'])
            elif action == 'del_contact':
                self.db.del_contact(massage['user_login'], massage['login_for_del'])
          
        return data

    def resend_massage(self):
        for sock in self.w:
            for massage in self.massages:
                if massage['reciever'] == self.clients[sock]:
                    sock.send(json.dumps(massage).encode('utf-8'))

    def get_contacts(self, massage : dict) -> dict:
        contacts_id_list = self.db.session.query(self.db.Contacts_list).filter_by(id=self.db.get_id_by_login(massage['user_login'])).all()
        contacts_nick_list = []
        for i in contacts_id_list:
            contacts_nick_list.append(self.db.session.query(self.db.User).filter_by(id=i.contact_id).first().login)
        contacts = {'action': 'get_contacts', 'response' : '202', "reciever" : massage['user_login'], 'alert' : contacts_nick_list}
        return contacts
            
        
    def start(self):

        self.db = ServerDataBase()

        print('MY Server RUN ^^^ ', end='')

        self.clients = {}

        srv_connect = (str(self.ip_addr), self.ip_port)
        print(srv_connect)
        self.srv_soc = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM - TCP
        self.srv_soc.bind((self.ip_addr, self.ip_port))  # ( aдрес, порт )
        self.srv_soc.listen(5)  # одновременно обслуживает не более 5 запросов
        self.srv_soc.settimeout(0.5)
        self.srv_soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # для быстрого автовысвобождения порта

        while True:
            try:
                conn, addr = self.srv_soc.accept()  # Проверка подключений
            except OSError as e:
                pass  # timeout вышел
            else:
                presence_massage = json.loads(conn.recv(256).decode('utf-8'))
                conn.send(json.dumps({'action' : 'presence_answer', 'time' : time.time(), 'alert' : '200'}).encode('utf-8'))
                print("Получен запрос на соединение от %s" % str(addr))
                self.clients[conn] = presence_massage['nick_name']
                
                # добавление подключившегося клиента в список пользователей,
                # в теле функции предусмотренно если клиент не новый
                self.db.add_user(presence_massage['nick_name'])

                #запись в историю при подключении
                self.db.history(
                    self.db.get_id_by_login(presence_massage['nick_name']),
                    conn.getpeername()[0]
                )

                
            finally:
                # Проверить наличие событий ввода-вывода
                self.massages = []
                wait = 3
                self.r = []
                self.w = []
                self.r, self.w, e = select.select(self.clients.keys(), self.clients.keys(), [], wait)

                # отладочные выводы
                print('передающие сокеты:')
                for sock in self.r:
                    print(sock.getpeername())
                print('принимающие сокеты:')
                for sock in self.w:
                    print(sock.getpeername())
                print()

                if self.r:  
                    self.massages = self.read_massages()  

                if self.massages:
                    self.resend_massage()
                
        

if __name__ == '__main__':
    Server1 = Server('localhost', 7777)
    Server1.start()
   


