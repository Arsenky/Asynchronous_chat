import subprocess

# Задание №1

print()
print('Задание 1')

a = "разработка"
b = "сокет"
c = "декоратор"

for el in [a, b, c]:
    print(el, type(el))

print()

a = "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
b = "\u0441\u043e\u043a\u0435\u0442"
c = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"

for el in [a, b, c]:
    print(el, type(el))

# Задани №2

print()
print('Задание 2')

a = b'class'
b = b'function'
c = b'method'

for el in [a, b, c]:
    print(el, type(el), len(el))

# Задание №3

print()
print('Задание 3')

for el in ('attribute', 'класс', 'функция', 'type'):
    try:
        print(bytes(el, encoding='ascii'))
    except UnicodeEncodeError:
        print(f"Слово '{el}' невозможно записать в виде байтовой строки")

# Задание №4

print()
print('Задание 4')

for el in ["разработка", "администрирование", "protocol", "standard"]:
    b_code = el.encode()
    print(el.encode())
    print(b_code.decode())

# Задание №5

print()
print('Задание 5')

subproc_ping = subprocess.Popen(['ping', 'yandex.ru'],  stdout=subprocess.PIPE) 
 
i = 0
for line in subproc_ping.stdout: 
    print(line.decode("utf-8"))

    # у меня почему то вывод продолжался бесконечно, ограничил вручную до 4-х строк
    if i>3:
        break
    i+=1

subproc_ping = subprocess.Popen(['ping', 'youtube.com'],  stdout=subprocess.PIPE) 
 
i = 0
for line in subproc_ping.stdout: 
    print(line.decode("utf-8"))

    # у меня почему то вывод продолжался бесконечно, ограничил вручную до 4-х строк
    if i>3:
        break
    i+=1

# Не столкнулся с кирилицей, так как работал на ubuntu. Возможные ошибки, описанные в методичке, учту.

# Задание №6

print()
print('Задание 6')

f_n = open("test_file.txt","r") 
f_n.close()
print(f_n)

with open('test_file.txt', encoding='utf-8') as file:
    for line in file.read():
        print(line)
