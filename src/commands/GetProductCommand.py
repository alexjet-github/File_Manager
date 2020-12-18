import re
import sys

from src.commands.AbstractCommand import AbstractCommand


class GetProductCommand(AbstractCommand):
    def __init__(self):
        self._match = None

    @property
    def name(self):
        return 'GET_PRODUCT'

    @property
    def help(self) -> str:
        return 'Calculates the product of the given values.'

    def can_execute(self, command: str) -> bool:
        self._match = re.search(rf'^{self.name} (\d+) (\d+)$', command)
        return bool(self._match)

    def execute(self):
        sys.stdout.write(
            f'{int(self._match.group(1)) * int(self._match.group(2))}\n'
        )