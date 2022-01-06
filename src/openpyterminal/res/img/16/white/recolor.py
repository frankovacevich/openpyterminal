import os
for file in os.listdir("."):
	if file != "recolor.py":

		w = open(file, "r")
		wt = w.read()
		wt = wt.replace("rgb(0%,0%,0%)","rgb(100%,100%,100%)")
		w.close()

		w = open(file, "w")
		w.write(wt)
		w.close()
