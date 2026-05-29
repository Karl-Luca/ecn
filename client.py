import asyncio
import socket
import sys

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import QuicConnection


SERVER_IP = sys.argv[1]

class ClientProtocol(QuicConnectionProtocol):
    async def send_data(self):
        stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(stream_id, b"Hello from client", end_stream=True)
        self.transmit()


async def run():
    loop = asyncio.get_event_loop()

    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x02)  # ECT(0)
    print("Socket TOS set to 0x02 (ECT(0))")
    print("Client UDP socket:", sock.getsockname())

    sock.setblocking(False)

    sock.bind(("0.0.0.0", 0))

    quic = QuicConnection(configuration=configuration)

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ClientProtocol(quic),
        sock=sock,
    )

    quic.connect((SERVER_IP, 4433), now=loop.time())
    protocol.transmit()

    await protocol.send_data()

    await asyncio.sleep(2)

    transport.close()


if __name__ == "__main__":
    asyncio.run(run())