import csv

FILE = "uart_dump9"


with open(FILE+".csv") as csvfile:
    next(csvfile)  # skip headers
    reader = csv.reader(csvfile)
    raw = list([[float(x[2]), int(x[4], 16)] for x in reader])

packets = []
packets_i = 0
last_t = 0
for t, byte in raw:
    if t - last_t > 0.00016:
        packets.append([])
        packets_i += 1
    last_t = t
    packets[packets_i-1].append(byte)

for packet in packets:
    if packet[2] == 0xFF:  # false trigger
        packet.pop(2)

pretty_print = "\n".join([" ".join([hex(x).upper()[2:].rjust(
    2, '0') for x in packet]) for packet in packets])
with open(FILE+".txt", "w") as f:
    f.write(pretty_print)
print(pretty_print)
