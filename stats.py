import os
import sys
import json

strr = "gen number,max_steps\n"
for f in os.listdir(sys.argv[1]):
    gn = f[1:]
    strr += str(gn)+","
    with open(sys.argv[1]+"/"+f+"/stats.json") as file:
        stats=json.load(file)
        strr+=str(stats["max_steps"])+"\n"

print(strr)

