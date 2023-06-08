import dis
from socket import socket

class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):

        # использование сокетов для работы по TCP (наличие мотодов для работы с сокетом)
        if not 'send_massage' in clsdict.keys() or not 'receive_massage' in clsdict.keys():
            raise TypeError('У клиента отсутствует метод для отправки или метод для приёма сообщений!')
       
        for key, value in clsdict.items():

            # Пропустить специальные и частные методы
            if key.startswith("__"):
                continue

            if 'socket.socket' in str(type(value)):
                raise TypeError ('В классе создаётся сокет на уровне класса!')

            try:
                func_data = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for i in func_data:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval in ('listen', 'accept'):
                            raise TypeError(f'Недопустимая операция с сокетом - "{i.argval}" в методе {key}')

        type.__init__(self, clsname, bases, clsdict)

class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):

        # # использование сокетов для работы по TCP (наличие мотодов для работы с сокетом)
        # if not 'send_massage' in clsdict.keys() or not 'receive_massage' in clsdict.keys():
        #     raise TypeError('У клиента отсутствует метод для отправки или метод для приёма сообщений!')
       
        for key, value in clsdict.items():
            attrs = set()

            # Пропустить специальные и частные методы
            if key.startswith("__"):
                continue

            try:
                func_data = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for i in func_data:
                    if i.opname == 'LOAD_METHOD':
                        if i.argval in ('connect'):
                            raise TypeError(f'Недопустимая операция с сокетом - "{i.argval}" в методе {key}')

                
                    if i.opname == 'LOAD_GLOBAL':
                        if not i.argval in attrs:
                            attrs.add(i.argval)
                            
        if (not 'AF_INET' in attrs) or (not 'SOCK_STREAM' in attrs):
            raise TypeError('Некорректная инициализация сокета')
                            

        type.__init__(self, clsname, bases, clsdict)
