import asyncio


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost, encoding='utf-8'):
        self.message = message
        self.on_con_lost = on_con_lost
        self.encoding = encoding

    def connection_made(self, transport):
        msgBuffer = self.message.encode(self.encoding)
        print(len(msgBuffer))
        transport.write(msgBuffer)
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode(self.encoding)))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)

    def sendMessage(self, msg):
        self.transport.write(self.message.encode(self.encoding))
        print('Data sent: {!r}'.format(self.message))


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 8080)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())