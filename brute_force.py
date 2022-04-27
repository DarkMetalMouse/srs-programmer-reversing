import serial
import struct
import binascii
import time


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    r = s.read(len(bytes))
    assert r == bytes


def checksum(bytes: bytearray) -> bytearray:
    return struct.pack("B", (~sum(bytes)) & 0xFF)


def send_data(s: serial.Serial, bytes: bytearray):
    loopback_write(s, b'\xFF\xFF' + bytes + checksum(bytes))


def wait_for_bytes(s: serial.Serial, bytes: bytearray):
    assert s.read(len(bytes)) == bytes


s = serial.Serial("COM3", 77170)
# s.timeout = 0.025

# for i in range(0xFFFF):
#     send_data(s, b"\x01\x04\x02" + struct.pack(">H", i))
#     r = s.read(100)
#     if r:
#         print(f"{i}: {r}")

# prev = b''
# for i in range(0xFF):
#     for j in range(1, 0xFF):
#         send_data(s, b"\x01\x04\x02" + struct.pack("BB", i, j))
#         r = s.read(100)
#         if not r:
#             break
#         prev = r
#     print(
#         f"{hex(i)[2:].upper().rjust(2,'0')}: {binascii.hexlify(prev, ' ').decode('utf-8').upper()}")

data = b""
send_data(s, b"\x01\x04\x02\x00\x39")
data += s.read(63)[5:-1]
time.sleep(0.4)
send_data(s, b"\x01\x04\x02\x39\x0b")
data += s.read(17)[5:-1]
print(binascii.hexlify(data, ' ').decode('utf-8').upper())
