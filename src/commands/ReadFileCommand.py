import os
import re
import sys

from src.commands.AbstractCommand import AbstractCommand


class ReadFileCommand(AbstractCommand):
    def __init__(self):
        self._match = None

    @property
    def name(self) -> str:
        return 'READ_FILE'

    @property
    def help(self) -> str:
        return 'Print the content of the given file.'

    def can_execute(self, command: str) -> bool:
        self._match = re.search(rf'^{self.name} (.*)$', command)
        return bool(self._match)

    def execute(self):
        filename = self._match.group(1)

        with open(filename, 'rb') as f:
            sys.stdout.write(f.read(os.stat(filename).st_size).decode())