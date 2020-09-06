import os
import sys
import json
import config
import solver

config.sssa = 10000

for d in os.listdir(sys.argv[1]):
    for f in os.listdir(sys.argv[1]+"/"+d):
        with open (sys.argv[1]+"/"+d+"/"+f) as file:
            data = json.load(file)
            if "nb_steps" in data and data["nb_steps"] == int(sys.argv[2]):
                print(d+"/"+f)
                sol = solver.astar_solve(data)
                seq = solver.getSequence(sol)
                print(d+"/"+f+" - "+seq)


