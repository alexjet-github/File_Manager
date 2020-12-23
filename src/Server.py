import asyncio
import logging

from asyncio.streams import StreamReader, StreamWriter
from src.commands.CommandFactory import CommandFactory


async def process(reader: StreamReader, writer: StreamWriter):
    host, port = writer.transport.get_extra_info('peername')
    logging.info(f'Client {host}:{port} is connected!')

    factory = CommandFactory(reader, writer)

    try:
        while True:
            line = (await reader.readline()).decode().strip()
            command = factory.get_command(line)

            # while True:
            #     line = input('=> ')
            #     command: AbstractCommand = factory.get_command(line)
            #     command.execute()

            await command.execute()
    except ConnectionResetError:
        writer.close()
        logging.info(f'Disconnected from {host}:{port}')


async def start_server(host, port):
    server = await asyncio.start_server(process, host, port)
    logging.info(f'Server started on {host}:{port}')

    async with server:
        await server.wait_closed()