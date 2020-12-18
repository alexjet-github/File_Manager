import sys

from asyncio.streams import StreamReader, StreamWriter
from src.commands.AbstractCommand import AbstractCommand
from src.commands.EchoCommand import EchoCommand
from src.commands.GetProductCommand import GetProductCommand
from src.commands.ReadFileCommand import ReadFileCommand

# class CommandFactory(object):
#     class __UnknownCommand(AbstractCommand):
#         async def execute(self):
#             self._writeline('Error: "Unknown command"')
#
#     _commands = {
#         'ECHO_START': EchoCommand,
#         'GET_PRODUCT': GetProductCommand,
#         'READ_FILE': ReadFileCommand,
#     }
#
#     def __init__(self, reader, writer):
#         self.__reader: StreamReader = reader
#         self.__writer: StreamWriter = writer
#
#     def get_command(self, command) -> AbstractCommand:
#         return self._commands.get(command, self.__UnknownCommand)(
#             self.__reader, self.__writer
#         )


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

    def __init__(self, reader, writer):
        self.__reader: StreamReader = reader
        self.__writer: StreamWriter = writer
        self.commands = [
            EchoCommand(),
            GetProductCommand(),
            ReadFileCommand(),
            self.__HelpCommand(self),
            self.__UnknownCommand(),
        ]

    # @property
    # def commands(self) -> dict:
    #     return {
    #         'echo_start': EchoCommand(),
    #         'get_product': GetProductCommand(),
    #         'read_file': ReadFileCommand(),
    #         'help': self.__HelpCommand(self),
    #     }

    # def __init__(self):
    #     self.commands = [
    #         EchoCommand(),
    #         GetProductCommand(),
    #         ReadFileCommand(),
    #         self.__HelpCommand(self),
    #         self.__UnknownCommand(),
    #     ]

    def get_command(self, line: str) -> AbstractCommand:
        for command in self.commands:
            if command.can_execute(line):
                 return command

    # def get_command(self, command) -> AbstractCommand:
    #     return self._commands.get(command, self.__UnknownCommand)(
    #         self.__reader, self.__writer
    #     )