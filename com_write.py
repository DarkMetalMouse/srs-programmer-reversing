import serial


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    assert s.read(len(bytes)) == bytes


s = serial.Serial("COM3", 77170)
s.inter_byte_timeout = 0.05
print(s.inter_byte_timeout)
loopback_write(s, bytearray.fromhex("FFFFFE0201FE"))
bytes = s.read(1000)
print(bytes)

loopback_write(s, bytearray.fromhex("FF FF 01 04 02 15 01 E2"))
bytes = s.read(1000)
print(bytes)

loopback_write(s, bytearray.fromhex("FF FF 01 04 03 34 00 C3"))
bytes = s.read(1000)
print(bytes)

loopback_write(s, bytearray.fromhex(
    "FF FF 01 2F 03 06 02 1E 00 05 00 0F 00 2D 00 00 00 00 0F 03 FC 00 00 00 00 41 03 C5 00 00 01 FF 01 00 02 09 C4 01 F4 02 8C 00 01 00 00 00 00 01 98 00 61"))
bytes = s.read(1000)
print(bytes)

loopback_write(s, bytearray.fromhex("FF FF 01 04 03 34 01 C2"))
bytes = s.read(1000)
print(bytes)
