from subprocess import PIPE, Popen, run

clients_number = input('Введите количество запускаемых клиентов: ')

for i in clients_number:
    with open('input_file.txt', 'r', encoding='utf-8') as f_in:
        with open('output_file.txt', 'w') as out_in:

            run(['python3', 'client.py', 'localhost'],
                stdout=out_in,
                stdin=f_in,
                )


