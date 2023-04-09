import re
import os
import csv
import json
import yaml

# обозначаю рабочий директорий для отладки
os.chdir('lesson_2')

# Задание 1


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

# чтение файлов
    for i in range(1, 4):
        info_file = open(f'info_{i}.txt', 'r')
        data = info_file.read()

        # изготовитель
        os_prod_list.append(
            (re.compile(r'Изготовитель системы:\s*\S*').findall(data))[0].split()[2])

        # ОС
        os_name_list.append(
            (re.compile(r'Название ОС:\s*\S*').findall(data))[0].split()[2])

        # код
        os_code_list.append(
            (re.compile(r'Код продукта:\s*\S*').findall(data))[0].split()[2])

        # тип ОС
        os_type_list.append(
            (re.compile(r'Тип системы:\s*\S*').findall(data))[0].split()[2])

    main_data = [["Изготовитель системы",
                  "Название ОС", "Код продукта", "Тип системы"]]

    for i in range(3):
        new_row = [os_prod_list[i], os_name_list[i],
                   os_code_list[i], os_type_list[i]]
        main_data.append(new_row)

    return (main_data)


def write_to_csv(csv_file_name):

    with open(csv_file_name, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data():
            f_n_writer.writerow(row)


write_to_csv('data_file.csv')

# Задание 2


def write_order_to_json(item, quantity, price, buyer, date):

    new_order = {"item": item, "quantity": quantity,
                 "price": price, "buyer": buyer, "date": date}

    with open('orders.json', 'r', encoding='utf-8') as f_n:
        data = json.load(f_n)

    data['orders'].append(new_order)

    with open('orders.json', 'w', encoding='utf-8') as f_n:
        json.dump(data, f_n, sort_keys=True, indent=4)

write_order_to_json('Workbook', 216, 144.50, " ООО 'Звезда'", "05.06.2023")

# Задание 3


def write_to_yaml():

    data = {"key1": [5, 6, 8], "key_2": 53, "key_3": {
        "key_1.1": '4¥', "key_1.2": '300§'}}

    with open('file.yaml', 'w', encoding='utf-8') as f_n:
        yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)


    with open('file.yaml', 'r', encoding='utf-8') as f_n:
        data_1 = yaml.load(f_n)

    print(data == data_1)

write_to_yaml()
