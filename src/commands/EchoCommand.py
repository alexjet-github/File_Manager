import sys

from src.commands.AbstractCommand import AbstractCommand


class EchoCommand(AbstractCommand):
    @property
    def name(self):
        return 'ECHO_START'

    @property
    def help(self) -> str:
        return 'Starts an echo loop.'

    def can_execute(self, command: str) -> bool:
        return command == self.name

    async def execute(self):
        while True:
            message = await self._readline()

            if message == 'ECHO_STOP':
                break

            self._writeline(message)
            # self._writeline(f'{message}".\n')