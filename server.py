import asyncio
import socket
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

async def handle_stream(reader, writer):
    data = await reader.read(1024)
    print("Received:", data)

    writer.write(b"Hello from server")
    await writer.drain()
    writer.close()
    await writer.wait_closed()

def stream_handler(reader, writer):
    asyncio.create_task(handle_stream(reader, writer))

async def run():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain("cert.pem", "key.pem")

    server = await serve(
        "127.0.0.1",
        4433,
        configuration=configuration,
        stream_handler=stream_handler,
    )

    print("Server started")

    await asyncio.sleep(0.1)

    transport = server._transport
    sock = transport.get_extra_info("socket")

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x02)

    print("Server TOS set to:",
          sock.getsockopt(socket.IPPROTO_IP, socket.IP_TOS))

    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(run())