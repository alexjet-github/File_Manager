import os
import sys

from configparser import ConfigParser

class ApplicationSettings(object):
    _config_file_name = 'settings.conf'

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        self._config = ConfigParser()

        if not os.path.exists(self._local_config_path()):
            print('INFO. First start - config file does not exist')
            self._create_default_local_config()

        self._config.read(self._local_config_path())

    @property
    def settings(self) -> dict:
        return {
            'file_server_host': self.file_server_host,
            'file_server_port': self.file_server_port,
            'web_server_port': self.web_server_port,
            'root_login': self.root_login,
            'root_password': self.root_password,
            'settings_resuming': self.settings_resuming,
            'settings_web_enable': self.settings_web_enable,
            'settings_log_file': self.settings_log_file,
        }

    @property
    def file_server_host(self):
        return self._get_value('Network', 'file_server_host')

    @property
    def file_server_port(self):
        return self._get_value('Network', 'file_server_port')

    @property
    def web_server_port(self):
        return self._get_value('Network', 'web_server_port')

    @property
    def root_login(self):
        return self._get_value('Root', 'login')

    @property
    def root_password(self):
        return self._get_value('Root', 'password')

    @property
    def settings_resuming(self):
        """Включение/выключение функции докачки."""
        return self._get_value('Settings', 'resuming')

    @property
    def settings_web_enable(self):
        """Включение/выключение веб-интерфейса."""
        return self._get_value('Settings', 'web_enable')

    @property
    def settings_log_file(self):
        """Имя лог-файла сервера."""
        return self._get_value('Settings', 'log_file')

    def _create_default_local_config(self):
        self._config['Network'] = {}
        self._config['Network']['file_server_host'] = '127.0.0.1'
        self._config['Network']['file_server_port'] = '3223'
        self._config['Network']['web_server_port'] = '8080'

        self._config['Root'] = {}
        self._config['Root']['login'] = 'root'
        self._config['Root']['password'] = 'password'

        self._config['Settings'] = {}
        self._config['Settings']['resuming'] = 'yes'
        self._config['Settings']['web_enable'] = 'yes'
        self._config['Settings']['log_file'] = 'log.txt'

        path = self._local_config_path()
        basedir = os.path.dirname(path)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

        with open(path, 'w') as config_file:
            self._config.write(config_file)
            print('INFO. Create default local config - see "log.txt"')

    def _get_value(self, section, key):
        try:
            return self._config[section][key]
        except KeyError:
            print('Invalid application settings file')
            sys.exit(1)

    @staticmethod
    def _home_directory():
        return os.path.expanduser('')

    @classmethod
    def _local_config_path(cls):
        return os.path.join(
            cls._home_directory(),
            '.',
            cls._config_file_name
        )