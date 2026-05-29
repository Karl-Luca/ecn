import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 0x02)

sock.bind(("0.0.0.0", 0))

payload = b"x" * 1200

while True:
    sock.sendto(payload, ("127.0.0.1", 9999))
    time.sleep(1)