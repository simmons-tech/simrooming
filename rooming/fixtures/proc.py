fin = open("fixture.json", 'r')
lines = fin.read()[2:-2].split("}, {")
yes = [line for line in lines if '"model": "rooming' in line]
print yes
print
out = "[{" + "}, {".join(yes) + "}]"
print out
fout = open("roomformat.json", "w")
fout.write(out)

entries = [line.split(", ") for line in lines]
derp = set([])
for entry in entries:
    derp.add(entry[1].split(": ")[1])
print derp
