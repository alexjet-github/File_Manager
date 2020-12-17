import logging
import sys
import asyncio

from src.ApplicationSettings import ApplicationSettings
from src.Network import start_server

app_set = ApplicationSettings()

def logger_config():
    """Функция конфигурации логгера"""
    _filename = app_set.settings_log_file
    _format = '%(asctime)s %(levelname)s: %(message)s'
    _level = logging.INFO
    _datefmt = '%Y-%m-%d %H:%M:%S'

    if _filename:
        logging.basicConfig(filename=_filename, format=_format, datefmt=_datefmt, level=_level)
        logging.info('Start logging')
    else:
        logging.basicConfig(filename='log.txt', format=_format, datefmt=_datefmt, level=_level)
        logging.warning('Start logging. The name of the log file in the settings.conf is empty!')

def file_change(_self, type, string):
    try:
        f = open(_self, type)
        if type == 'r':
            return f.read()
        else:
            f.write(string)
    except IOError:
        print('%_self does not exist!')
    finally:
        f.close()

if __name__ == '__main__':
    logger_config()

    logging.info('Default local config:')
    for key, value in app_set.settings.items():
        string = f'\t\t\t\t\t{key}: {value}\n'
        file_change('log.txt', 'a', string)

    host = app_set.file_server_host
    port = app_set.file_server_port
    asyncio.run(start_server(host,port))

    sys.stdout.write(file_change('log.txt', 'r', 0))
