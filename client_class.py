# -*- coding: UTF-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, qApp
from client_form import Ui_MainWindow
import sys
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import time
import datetime
import json
import logging
import log.client_log_config, log.server_log_config
from log.log_decorator import log
import threading
from metaclasses import ClientVerifier
from client_database import ClientDataBase
from sqlalchemy import or_, and_

client_logger = logging.getLogger('client')

class Client(metaclass = ClientVerifier):
    """Описание класса клиента"""
    
    def __init__(self, ip_addr, ip_port) -> None:
        self.ip_addr = ip_addr
        self.ip_port = ip_port
        self.nick_name = ''
        self.clt_soc = None

    @log
    def create_presence_massage(self) -> dict:
            connection_massage = { "action" : "presence", "time": time.time(), "nick_name" : self.nick_name, "password" : self.password} 
            client_logger.info(f'Сформированно сообщение о присутствии серверу')
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
                if massage['action'] == 'massage':
                    print(f"\nПринято сообщение : {massage['user_massage']}")
                    self.db.history(massage['sender'], massage['reciever'], massage['user_massage'])
                elif massage['action'] == 'get_contacts':
                    self.contact_list = massage['alert']
                

    # функция отправки сигнала серверу об отключении клиента
    @log
    def send_quit_signal(self):
        """функция отправки сигнала серверу об отключении клиента"""
        signal = { "action": "quit", "time": time.time()}
        self.clt_soc.send((json.dumps(signal)).encode('utf-8'))

    # функция отправки сигнала на остановку сервера
    @log
    def send_stop_signal(self):
        signal = { "action": "stop", "time": time.time()}
        self.clt_soc.send((json.dumps(signal)).encode('utf-8'))

    def send_massage(self, reciever, text):
        massage = { "action" : "massage", "time" : time.time(), "sender": self.nick_name, "reciever" : reciever, "user_massage" : text}
        self.clt_soc.send((json.dumps(massage)).encode('utf-8'))

    def get_contacts(self):
        massage = {
            "action": "get_contacts",
            "time": time.time(),
            "user_login": self.nick_name
            }
        self.clt_soc.send((json.dumps(massage)).encode('utf-8'))

    def add_contact(self, login_for_add):
        massage = {
            "action": "add_contact",
            "time": time.time(),
            "user_login": self.nick_name,
            'login_for_add' : login_for_add
            }
        self.clt_soc.send((json.dumps(massage)).encode('utf-8'))
        
    def del_contact(self, login_for_del):
        massage = {
            "action": "del_contact",
            'user_login': self.nick_name,
            'login_for_del' : login_for_del
            }
        self.clt_soc.send((json.dumps(massage)).encode('utf-8'))


    def start(self):
        self.nick_name = ui.nick_lineEdit.text()
        self.password = ui.password_lineEdit.text()
        self.contact_list = None
        self.db = ClientDataBase()
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
            presence_answer = json.loads(self.clt_soc.recv(256).decode('utf-8'))
            if presence_answer['alert'] == '200':
                print('Успешное подключение к серверу')
                self.get_contacts()
            elif presence_answer['alert'] == '401':
                print('Неверный пороль')
                exit(1)
   
        receiver = threading.Thread(target=self.receive_massage, args=())
        receiver.daemon = True
        receiver.start()

        # user_console.join()


def add_contact():
    ui.contacts_list.addItem(f'{ui.add_contact_lineEdit.text()}')
    Client1.add_contact(ui.add_contact_lineEdit.text())

def del_contact():
    Client1.del_contact(ui.contacts_list.currentItem().text())
    ui.contacts_list.takeItem(ui.contacts_list.currentIndex().row())

def start():
    ui.startbutton.hide()
    ui.nick_lineEdit.hide()
    ui.password_lineEdit.hide()
    ui.password_label.hide()
    ui.exit_Button.show()
    Client1.start()
    ui.start_nick_label.setText(f'Ваш ник: {Client1.nick_name}')

    while Client1.contact_list == None:
        time.sleep(0.1)
    else:
        for contact in Client1.contact_list:
            ui.contacts_list.addItem(f'{contact}')

def massage():
    Client1.send_massage(ui.reciever.text(), ui.massage_text.toPlainText())

def chat_switched():
    ui.chat_window.clear()
    print(Client1.nick_name, ui.contacts_list.currentItem().text())
    chat = Client1.db.session.query(Client1.db.Massages_history).filter(or_(
        (and_(Client1.db.Massages_history.sender == ui.contacts_list.currentItem().text(), Client1.db.Massages_history.reciever == Client1.nick_name)),
        (and_(Client1.db.Massages_history.sender == Client1.nick_name, Client1.db.Massages_history.reciever == ui.contacts_list.currentItem().text())))
        ).order_by(Client1.db.Massages_history.time).all()

    ui.chat_window.cursorForPosition(QtCore.QPoint(1, 2))
    for msg in chat:
        
        if msg.sender == Client1.nick_name:
            time = msg.time.strftime('%Y-%m-%d %H:%M:%S')
            ui.chat_window.append(f"{time}   {msg.sender}:  {msg.text}")
            ui.chat_window.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif msg.sender != Client1.nick_name:
            time = msg.time.strftime('%Y-%m-%d %H:%M:%S')
            ui.chat_window.append(f"{msg.text}   :{msg.sender}  {time}")
            ui.chat_window.setAlignment(Qt.AlignmentFlag.AlignRight)

def exit():
    Client1.send_quit_signal()
    app.quit()
    
if __name__ == '__main__':
    Client1 = Client('localhost', 7777)

    app = QtWidgets.QApplication(sys.argv) 

    window = QMainWindow() 
    ui = Ui_MainWindow() 
    ui.setupUi(window)

    ui.startbutton.clicked.connect(start)
    ui.sendbutton.clicked.connect(massage)
    ui.contacts_list.doubleClicked.connect(chat_switched)
    ui.add_contact_button.clicked.connect(add_contact)
    ui.del_contact_button.clicked.connect(del_contact)
    ui.exit_Button.clicked.connect(exit)

    window.show() 
    sys.exit(app.exec_())
     

   
   