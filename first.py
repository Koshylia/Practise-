import re
hand = open(r"E:\DZZ\practice\LC81810252016147LGN00\LC81810252016147LGN00_MTL.txt")

for line in hand:
    line = line.rstrip()
    stuff = re.findall('RADIANCE_MAXIMUM_BAND_10 = ([0-9.]+)', line)
    if len(stuff) != 1: continue
    num = float(stuff[0])
    print (num)
