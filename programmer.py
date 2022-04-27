import serial
import struct
import time


def map(x1, y1, x2, y2, x):
    return (y2-y1)/(x2-x1)*(x-x1)+y1


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    assert s.read(len(bytes)) == bytes


def checksum(bytes: bytearray) -> bytearray:
    return struct.pack("B", (~sum(bytes)) & 0xFF)


def send_data(s: serial.Serial, bytes: bytearray):
    loopback_write(s, b'\xFF\xFF' + bytes + checksum(bytes))


def wait_for_bytes(s: serial.Serial, bytes: bytearray):
    assert s.read(len(bytes)) == bytes


continuous_mode = True
left_angle = -90  # (-135, 0)
right_angle = 90  # (1, 135)
left_adc = round(map(0, 512, -135, 65, left_angle))
right_adc = round(map(0, 512, 135, 965, right_angle))

left = int(map(65, 1000, 411, 232, left_adc))
right = int(map(965, 1000, 611, 213, right_adc))

s = serial.Serial("COM3", 77170)

# loopback_write(s, bytearray.fromhex("FF FF FE 02 01 FE"))
# wait_for_bytes(s, bytearray.fromhex("FF FF 01 02 00 FC"))
# time.sleep(0.02)

# loopback_write(s, bytearray.fromhex("FF FF 01 04 02 15 01 E2"))
# r = s.read(7)
# assert (r.startswith(bytearray.fromhex("FF FF 01 03 00")) and
#         (r.endswith(bytearray.fromhex("00 FB"))  # Current state is servo
#          or r.endswith(bytearray.fromhex("01 FA"))))  # Current state is continuous
# time.sleep(0.02)

loopback_write(s, bytearray.fromhex("FF FF 01 04 03 34 00 C3"))
wait_for_bytes(s, bytearray.fromhex("FF FF 01 02 00 FC"))
time.sleep(0.02)

if continuous_mode:
    loopback_write(s, bytearray.fromhex(
        "FF FF 01 2F 03 06 32 14 00 05 00 0A 00 0A 00 1E 00 00 00 03 FF 01 00 00 00 41 03 C5 01 F4 01 FF 00 00 02 06 0E 05 AA 03 E8 00 14 00 00 00 00 03 E8 00 99"))
else:
    send_data(s,
              bytearray.fromhex(
                  "01 2F 03 06 02 1E 00 05 00 0F 00 2D 00 00 00 00 0F 03 FC 00 00 00 00 41 03 C5 00 00 01 FF 01 00 02 09 C4 01 F4")
              + struct.pack(">H", left)
              + bytearray.fromhex("00 01 00 00 00 00")
              + struct.pack(">H", right)
              + bytearray.fromhex("00"))
wait_for_bytes(s, bytearray.fromhex("FF FF 01 02 00 FC"))
time.sleep(0.02)

# loopback_write(s, bytearray.fromhex("FF FF 01 04 03 34 01 C2"))
# wait_for_bytes(s, bytearray.fromhex("FF FF 01 02 00 FC"))
