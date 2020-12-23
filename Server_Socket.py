import socket
import sys
import os
import re
from abc import abstractmethod


class AbstractCommand(object):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def can_execute(self, command: str) -> bool:
        pass

    @abstractmethod
    def execute(self, command: str):
        pass


class EchoCommand(AbstractCommand):
    def __init__(self):
        self._command = None

    @property
    def name(self):
        return 'echo_start'

    @property
    def help(self) -> str:
        return 'Starts an echo loop'

    def can_execute(self, command: str) -> bool:
        # Переходим в цикл True если команда совпадает с именем
        if command == self.name:
            return True

    def execute(self):
        while True:
            # message = self._command
            message = file.readline()

            if message.strip() == 'echo_stop':
                break

            return message


class GetProductCommand(AbstractCommand):
    def __init__(self):
        self._match = None

    @property
    def name(self):
        return 'get_product'

    @property
    def help(self) -> str:
        return 'Calculates the product of the given values'

    def can_execute(self, command: str) -> bool:
        self._match = re.search(rf'^{self.name} (\d+) (\d+)$', command)
        return bool(self._match)

    def execute(self):
        return (
            f'{int(self._match.group(1)) * int(self._match.group(2))}\n'
        )


class ReadFileCommand(AbstractCommand):
    def __init__(self):
        self._match = None

    @property
    def name(self) -> str:
        return 'read_file'

    @property
    def help(self) -> str:
        return 'Print the content of the given file'

    def can_execute(self, command: str) -> bool:
        self._match = re.search(rf'^{self.name} (.*)$', command)
        return bool(self._match)

    def execute(self):
        filename = self._match.group(1)

        with open(filename, 'rb') as f:
            sys.stdout.write(f.read(os.stat(filename).st_size).decode())


class CommandFactory(object):
    class __HelpCommand(AbstractCommand):
        def __init__(self, factory):
            self._factory = factory

        @property
        def name(self) -> str:
            return 'help'

        @property
        def help(self) -> str:
            return 'Prints this help'

        def can_execute(self, command: str) -> bool:
            return command == self.name

        def execute(self):
            try:
                for command in self._factory.commands:
                    return f'"{command.name}" - {command.help}'
            except NotImplementedError:
                pass

    class __UnknownCommand(AbstractCommand):
        def __init__(self):
            self._command = None

        @property
        def name(self) -> str:
            raise NotImplementedError

        @property
        def help(self) -> str:
            raise NotImplementedError

        def can_execute(self, command: str) -> bool:
            self._command = command
            return True

        def execute(self):
            if self._command == '':
                return
            else:
                return f'Unknown command: {self._command}'

    def __init__(self):
        self.commands = [
            EchoCommand(),
            GetProductCommand(),
            ReadFileCommand(),
            self.__HelpCommand(self),
            self.__UnknownCommand(),
        ]

    def get_command(self, line: str) -> AbstractCommand:
        for command in self.commands:
            if command.can_execute(line):
                return command


# Main event loop
def reactor(host, port):
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    print(f'Server up, running, and waiting for call on {host} {port}')

    try:
        while True:
            conn, cli_address = sock.accept()
            process_request(conn, cli_address)

    finally:
        sock.close()

def process_request(conn, cli_address):
    file = conn.makefile()

    print(f'Received connection from {cli_address}')
    conn.sendall(b'Hello! You are connected to a multiplayer server via a socket\n')

    factory = CommandFactory()

    try:
        while True:
            conn.sendall(b'> ')

            line = file.readline().rstrip()
            command: AbstractCommand = factory.get_command(line)
            out = command.execute()
            if(out != None):
                print(out)
                conn.sendall(b'%a\r\n' %out)

    finally:
        print(f'{cli_address} quit')
        file.close()
        conn.close()

if __name__ == '__main__':
    reactor('localhost', 8080)