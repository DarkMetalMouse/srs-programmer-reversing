import serial
import struct
import time
import sys


def map(x1, y1, x2, y2, x) -> int:
    return (x-x1)*(y2-y1)//(x2-x1)+y1


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    wait_for_bytes(s, bytes)


def checksum(bytes: bytearray) -> bytearray:
    return struct.pack("B", (~sum(bytes)) & 0xFF)


def send_data(s: serial.Serial, bytes: bytearray):
    loopback_write(s, b'\xFF\xFF' + bytes + checksum(bytes))


def wait_for_bytes(s: serial.Serial, bytes: bytearray):
    if s.read(len(bytes)) != bytes:
        print("Error connecting to servo")
        sys.exit()


def srs_read_config(s: serial.Serial):
    loopback_write(s, bytearray.fromhex("FF FF 01 04 02 15 01 E2"))

    r = s.read(7)
    if (r[5] == 1):
        print("continuos mode")
    elif (r[5] == 0):
        print("servo mode")
        send_data(s, bytearray.fromhex("01 04 02 27 0A"))
        r = s.read(16)
        left_angle = map(1000, -135, 0, 0, (r[5] << 8) + r[6])
        right_angle = map(1000, 135, 0, 0, (r[13] << 8) + r[14])
        print(f"left = {left_angle}, right = {right_angle}")
    else:
        print("Error reading servo mode")
    # assert (r.startswith(bytearray.fromhex("FF FF 01 03 00")) and
    #         (r.endswith(bytearray.fromhex("00 FB"))  # Current state is servo
    #          or r.endswith(bytearray.fromhex("01 FA"))))  # Current state is continuous
    # time.sleep(0.02)


def srs_program(s: serial.Serial, left_angle: int, right_angle: int, continuous_mode: bool):

    left = map(-135, 1000, 0, 0, left_angle)
    right = map(135, 1000, 0, 0, right_angle)

    print("programming...")

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
    print("done")



def usage():
    print("Usage: python ./programmer.py <COMn> <r|read> | <c|continuos> | <min angle> <max angle>")
    sys.exit(1)


def is_int(s):
    """ Returns True is string is an int. """
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    left_angle = -135  # (-135, 0)
    right_angle = 135  # (1, 135)
    continuous_mode = False
    read_config = False

    if (len(sys.argv) < 2):
        usage()
    if (len(sys.argv) != 2):  # Factory reset
        if (sys.argv[2].lower() in ["c", "continuos"]):
            if (len(sys.argv) != 3):
                usage()
            continuous_mode = True
        elif (sys.argv[2].lower() in ["r", "read"]):
            read_config = True
        else:
            if (len(sys.argv) != 4 or not is_int(sys.argv[2]) or not is_int(sys.argv[3])):
                usage()
            continuous_mode = False
            left_angle = int(sys.argv[2])
            right_angle = int(sys.argv[3])
            if (not (-135 <= left_angle <= 0 and 1 <= right_angle <= 135)):
                print("Left angle must be in range (-135,0) and right (1,135)")
                sys.exit(1)
    s = None
    try:
        s = serial.Serial(sys.argv[1], 77170)
    except serial.SerialException as e:
        print("error opening serial port:\n" + str(e))
        sys.exit(1)
    s.timeout = 1

    if (read_config):
        srs_read_config(s)
    else:
        srs_program(s, left_angle, right_angle, continuous_mode)
