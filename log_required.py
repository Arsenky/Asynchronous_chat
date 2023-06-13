def log_ruauired(func):
    """Декоратор проверяющий, что запрос происходит от авторизированого клиента."""
    def out_func(*args, **kwargs):
        print(locals()['args'])
        server = locals()['args'][0] # объект класса принятый функцией через self
        # декоратор проверяет что список сокетов 
        for sock in server.r:
            if not (sock in server.clients.keys()):
                raise TypeError(f'Сокет {sock} не авторезирован') 
        return func(*args, **kwargs)
    return out_func