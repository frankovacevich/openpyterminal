al = open("all.txt", "r")
a = al.read().split(".svg")
al.close()
print(len(a))

b = []

import os
for file in os.listdir("."):
    b.append(file.replace(".svg", ""))

print([x for x in a if x not in b])
