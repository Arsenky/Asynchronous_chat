import unittest
from socket import socket, AF_INET, SOCK_STREAM
from server import receive_massage
from client import send_presence_massage, create_presence_massage
import time


class TestServer(unittest.TestCase):
    
    # функция приёма presence-сообщения, в тесте симулируется и клиент и сервер
    def test_reseive_massage(self):
        srv_soc = socket(AF_INET, SOCK_STREAM) 
        srv_soc.bind(('localhost', 7777))
        srv_soc.listen(5)
        

        clt_soc = socket(AF_INET, SOCK_STREAM)
        clt_soc.connect(('localhost', 7777))
       
        client , addr = srv_soc.accept()

        send_presence_massage(clt_soc)

        client_massage = receive_massage(client)
        massage = { 
            "action":"presence",
            # невозможно получить одинаковый результат при вызове функции time(),
            # просто дублируем результат: 
            "time": client_massage["time"],
            "type":"status", 
            "user": { "account_name":"C0deMaver1ck", "status":"Yep, I am here!" } 
            }

        self.assertEqual(massage, client_massage)

if __name__ == '__main__':
    unittest.main()
