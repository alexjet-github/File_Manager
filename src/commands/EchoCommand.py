import sys

from AbstractCommand import AbstractCommand


class EchoCommand(AbstractCommand):
    @property
    def name(self):
        return 'ECHO_START'

    @property
    def help(self) -> str:
        return 'Starts an echo loop.'

    def can_execute(self, command: str) -> bool:
        return command == self.name

    def execute(self):
        while True:
            message = sys.stdin.readline()

            if message.strip() == 'ECHO_STOP':
                break

            sys.stdout.write(message)
