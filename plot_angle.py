import serial
import time
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def loopback_write(s: serial.Serial, bytes: bytearray):
    s.write(bytes)
    assert s.read(len(bytes)) == bytes


s = serial.Serial("COM3", 77170)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

max_data_len = 1000

data = []


def animate(i):
    loopback_write(s, bytearray.fromhex("FFFFFE04023B02BE"))
    bytes = s.read(8)
    pos = struct.unpack(">I", b'\x00\x00' + bytes[-3:-1])[0]
    print(pos)
    data.append(pos)
    if len(data) > max_data_len:
        data.pop(0)
    ax1.clear()
    ax1.set_ylim(0, 1 << 10)
    ax1.set_xlim(0, max_data_len)
    ax1.plot(data)


ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
