from abc import abstractmethod
from asyncio.streams import StreamReader, StreamWriter

class AbstractCommand(object):
    def __init__(self, reader, writer):
        self._reader: StreamReader = reader
        self._writer: StreamWriter = writer

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
    async def execute(self):
        pass

    async def _readline(self):
        return (await self._reader.readline()).decode().strip()

    def _writeline(self, line: str):
        self._writer.write((line + '\n').encode())