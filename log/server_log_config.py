import logging
import sys
from logging import handlers


server_logger = logging.Logger('server')

formatter =logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(message)s ")

rfh = handlers.TimedRotatingFileHandler('server.log', when="d", interval=1, encoding='utf-8', backupCount=5)
rfh.setLevel(logging.DEBUG) 
rfh.setFormatter(formatter)

sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(formatter)
sh.setLevel(logging.ERROR)

server_logger.addHandler(rfh)
server_logger.setLevel(logging.DEBUG)
server_logger.addHandler(sh)


