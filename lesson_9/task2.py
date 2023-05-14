from task1 import host_ping
from ipaddress import ip_address

def host_range_ping():
    while True:
        start_host = input('Введите начальный адрес (меньший): ')
        end_host = input('Введите конечный адрес (больший): ')

        # проверка на равенство первых трёк октетов
        equal_flag = 0
        for i in range(3):
            if start_host.split('.')[i] == end_host.split('.')[i]:
                equal_flag += 1

        if equal_flag != 3:
            print('Первые три октета не совпадают, повторите ввод.')
            continue

        if start_host.split('.')[3] > end_host.split('.')[3]:
            print('Второй введённый адрес меньше первого, повторите ввод.')
            continue

        if end_host.split('.')[3] == '255':
            print('Последний октет не может быть равен 255, повторите ввод.')
            continue
        
        break
    
    hosts_list = []
    current_ip = ip_address(start_host)
    while current_ip <= ip_address(end_host):
        hosts_list.append(current_ip)
        current_ip += 1

    host_ping(hosts_list)

if __name__ == '__main__':        
    host_range_ping()