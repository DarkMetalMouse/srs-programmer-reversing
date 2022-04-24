import csv

FILE = "dump1"


def reverse_byte(num):
    bits = 8
    rev = 0
    while bits != 0:
        bits -= 1
        rev <<= 1
        rev += num & 1
        num >>= 1
    return rev


with open(FILE+".csv") as csvfile:
    reader = csv.reader(csvfile)
    raw = list([[float(x[0]), int(x[1])] for x in reader])

rate = 1.3e-5
count = 0
raw_packets = [""]
raw_packets_i = 0
for i in range(len(raw)-1):
    timediff = raw[i+1][0] - raw[i][0]
    if(timediff > 1.3e-5 * 10):
        raw_packets_i += 1
        raw_packets.append("")
    else:
        amount = round(timediff/rate)
        raw_packets[raw_packets_i] += str(raw[i][1]) * amount

decoded_packets = []
for i, raw_packet in enumerate(raw_packets):
    decoded_packets.append([])
    for offset in range(0, len(raw_packet), 10):
        part = raw_packet[offset+1:offset+9].ljust(8, '1')

        decoded_packets[i].append(reverse_byte(int(part, 2)))

pretty_print = "\n".join([" ".join([hex(x).upper()[2:].rjust(
    2, '0') for x in packet]) for packet in decoded_packets])
with open(FILE+".txt", "w") as f:
    f.write(pretty_print)
print(pretty_print)
