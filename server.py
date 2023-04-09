# -*- coding: UTF-8 -*-

from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
import time
import json


def main(ip_addr, ip_port):
    print('MY Server RUN ^^^ ', end='')

    srv_connect = (str(ip_addr), int(ip_port))
    print(srv_connect)
    srv_soc = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM - TCP
    srv_soc.bind((ip_addr, ip_port))  # ( aдрес, порт )
    print()
    srv_soc.listen(5)  # одновременно обслуживает не более 5 запросов

    while True:
        print('--------------\nожидание приёма ')
        client, addr = srv_soc.accept()
        print('получаем запрос на соединение от ', addr)

        clt_massage = client.recv(256)
        action = json.loads(clt_massage.decode('utf-8'))['action']

        if action == 'presence':
            client.send(
                (json.dumps({"response": 200, "alert": "Успешное подключение"})).encode('utf-8')
                )
        elif action == 'quit':
            client.close()
            print('сеанс закрыт')

        

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
