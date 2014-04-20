grtsec = {"": 12, "8910C": 2, "8910B": 3, "8910A": 4, "7": 5, "6AB": 6, "5AB": 7, "56C": 8, "4AB": 9, "34C": 10, "23AB": 11}

fin = open("rooms.csv", "r")
lines = fin.read().split("\n")[:-1]
fin.close()
entries = [line.split("\t") for line in lines]
pk = 1
newentries = []
for entry in entries:
    occ = "2"
    grt = str(grtsec[entry[2]])
    if entry[2] == '':
        occ = "1"
    newentries.append('{"pk": ' + str(pk) + ', "model": "rooming.room", "fields":{"max_occupancy": ' + occ + ', "grt_section": ' + grt + ', "number": "' + entry[0] + '"}}')
    pk += 1
out = "[" + ", ".join(newentries) + "]"
fout = open("fixfinal.json", 'w')
fout.write(out)
fout.close()
