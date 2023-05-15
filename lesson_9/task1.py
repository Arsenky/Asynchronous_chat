from subprocess import Popen, PIPE
from ipaddress import ip_address
import re

hosts_list_raw = ['172.217.16.46',  # гугл
                  '5.255.255.70',  # яндекс
                  '196.72.87.73'  # несуществующий
                  ]

hosts_list = []
for host in hosts_list_raw:
    hosts_list.append(ip_address(host))


def host_ping(hosts_list):
    for host in hosts_list:
        p = Popen([f'ping -c 4 {host}'],  # UNIX
                  shell=True,  stdout=PIPE
                  )         
        out = p.stdout.read().decode('utf-8')

        match = re.search(r'\d received', out) # решил оиентироваться по количеству принятых пакетов, если оно не 0 то узел доступен
        if match[0][0] == '0':
            print(f'{host} - узел недоступен.')
        else:
            print(f'{host} - узел доступен.')
        

if __name__ == '__main__':
    host_ping(hosts_list)
