import sys

from AbstractCommand import AbstractCommand
from EchoCommand import EchoCommand
from GetProductCommand import GetProductCommand
from ReadFileCommand import ReadFileCommand


class CommandFactory(object):
    class __HelpCommand(AbstractCommand):
        def __init__(self, factory):
            self._factory = factory

        @property
        def name(self) -> str:
            return 'HELP'

        @property
        def help(self) -> str:
            return 'Prints this help.'

        def can_execute(self, command: str) -> bool:
            return command == self.name

        def execute(self):
            try:
                for command in self._factory.commands:
                    print(f'{command.name}: {command.help}')
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
            sys.stdout.write(f'Unknown command: "{self._command}".\n')

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
