import logging
import sys


client_logger = logging.Logger('client')

formatter =logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(message)s ")

fh = logging.FileHandler('client.log',  encoding='utf-8')
fh.setLevel(logging.DEBUG) 
fh.setFormatter(formatter)

sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(formatter)
sh.setLevel(logging.ERROR)



client_logger.addHandler(fh)
client_logger.setLevel(logging.DEBUG)
client_logger.addHandler(sh)

