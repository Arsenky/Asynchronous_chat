from subprocess import Popen, PIPE
from ipaddress import ip_address
import re
from tabulate import tabulate

# функция из задания 1 модифицируется для условия задачи 3
def host_ping(hosts_list): 
    reachable = []
    unreachable = []
    for host in hosts_list:
        p = Popen([f'ping -c 4 {host}'],  # UNIX
                  shell=True,  stdout=PIPE
                  )         
        out = p.stdout.read().decode('utf-8')

        match = re.search(r'\d received', out) # решил оиентироваться по количеству принятых пакетов, если оно не 0 то узел доступен
        if match[0][0] == '0':
            unreachable.append(str(host))
        else:
            reachable.append(str(host))
    
    return reachable, unreachable

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

    reachable, unreachable = host_ping(hosts_list)
    print(tabulate({'reachable' : reachable, 'unreachable' : unreachable}, headers = 'keys', tablefmt="grid"))

if __name__ == '__main__':        
    host_range_ping()