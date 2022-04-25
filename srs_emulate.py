import struct
import serial
import random


def map(x1, y1, x2, y2, x):
    return (y2-y1)/(x2-x1)*(x-x1)+y1


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    assert s.read(len(bytes)) == bytes


def checksum(bytes: bytearray) -> bytearray:
    return struct.pack("B", (~sum(bytes)) & 0xFF)


def send_data(s: serial.Serial, bytes: bytearray):
    loopback_write(s, b'\xFF\xFF' + bytes + checksum(bytes))


def send_adc(s: serial.Serial, num: int):
    send_data(s, b"\x01\x04\x00" + struct.pack(">H", num))


def wait_for_bytes(s: serial.Serial, bytes: bytearray):
    assert s.read(len(bytes)) == bytes


s = serial.Serial("COM3", 77170)
left_angle = random.randint(-135, -30)
right_angle = random.randint(30, 135)
left = round(map(0, 512, -135, 65, left_angle))
right = round(map(0, 512, 135, 965, right_angle))

print(left_angle, right_angle)
print(left, right)

wait_for_bytes(s, bytearray.fromhex("FF FF FE 04 02 3B 02 BE"))

send_adc(s, left)
wait_for_bytes(s, bytearray.fromhex("FF FF FE 04 02 3B 02 BE"))
send_adc(s, right)

wait_for_bytes(s, bytearray.fromhex("FF FF FE 02 01 FE"))

loopback_write(s, bytearray.fromhex("FF FF 01 02 00 FC"))

wait_for_bytes(s, bytearray.fromhex("FF FF 01 04 02 15 01 E2"))

loopback_write(s, bytearray.fromhex("FF FF 01 03 00 00 FB"))

wait_for_bytes(s, bytearray.fromhex("FF FF 01 04 03 34 00 C3"))

loopback_write(s, bytearray.fromhex("FF FF 01 02 00 FC"))

config = s.read(51)

loopback_write(s, bytearray.fromhex("FF FF 01 02 00 FC"))

wait_for_bytes(s, bytearray.fromhex("FF FF 01 04 03 34 01 C2"))

loopback_write(s, bytearray.fromhex("FF FF 01 02 00 FC"))

print(struct.unpack(">39xH6xH2x", config))

print((int(map(65, 1000, 411, 232, left)),
       int(map(965, 1000, 611, 213, right))))
