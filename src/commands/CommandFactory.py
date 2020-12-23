import sys
import logging

from asyncio.streams import StreamReader, StreamWriter
from src.commands.AbstractCommand import AbstractCommand
from src.commands.EchoCommand import EchoCommand
from src.commands.GetProductCommand import GetProductCommand
from src.commands.ReadFileCommand import ReadFileCommand


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

        async def execute(self):
             try:
                for command in self._factory.commands:
                    self._writeline(f'{command.name}: {command.help}\n')
                    print(f'{command.name}: {command.help}')
             except NotImplementedError:
                 pass

    class __UnknownCommand(AbstractCommand):
        def __init__(self):
            self.command = None

        @property
        def name(self) -> str:
            raise NotImplementedError

        @property
        def help(self) -> str:
            raise NotImplementedError

        def can_execute(self, command: str) -> bool:
            self.command = command
            return True

        async def execute(self):
            self._writeline(f'Unknown command: "{self.command}".')

    def __init__(self, reader, writer):
        self.get_from_client: StreamReader = reader
        self.send_to_client: StreamWriter = writer

    # @property
    # def commands(self) -> dict:
    #     return {
    #         # 'echo_start': EchoCommand(),
    #         # 'get_product': GetProductCommand(),
    #         # 'read_file': ReadFileCommand(),
    #         # 'help': self.__HelpCommand(self),
    #     }

    commands = {
        # 'help': self.__HelpCommand(),
        # 'ECHO_START': EchoCommand,
        # 'GET_PRODUCT': GetProductCommand,
        # 'READ_FILE': ReadFileCommand,
        # EchoCommand(),
        # GetProductCommand(),
        # ReadFileCommand(),
        # self.__HelpCommand(self),
        # self.__UnknownCommand()
    }

    def get_command(self, line) -> AbstractCommand:
        return self.commands.get(line, self.__UnknownCommand)(
            self.get_from_client, self.send_to_client
        )