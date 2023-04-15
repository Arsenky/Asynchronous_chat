import unittest
from socket import socket, AF_INET, SOCK_STREAM
import time
from client import create_presence_massage, send_presence_massage, receive_answer

class TestClient(unittest.TestCase):

    # функция генерации сообщения, 
    # просто сравниваем результат работы с готовым словарём
    def test_create_presence_massage(self):
        massage = create_presence_massage()
        self.assertEqual(massage, {
            "action": "presence",
            # невозможно получить одинаковый результат при вызове функции time(),
            # просто дублируем результат:
            "time": massage['time'], 
            "type": "status",
            "user": {"account_name": "C0deMaver1ck", "status": "Yep, I am here!"}
        }
        )

    # функция приёма ответа, тест работает при активном сервере, 
    # туда отправляется запрос и возвращается реальный ответ
    def test_reseive_answer(self):

        clt_soc = socket(AF_INET, SOCK_STREAM)
        clt_soc.connect(('localhost', 7777))

        send_presence_massage(clt_soc)
        massage = {"response": 200, "alert": "Успешное подключение"}

        self.assertEqual(massage, receive_answer(clt_soc))

        clt_soc.close()

if __name__ == '__main__':
    unittest.main()
