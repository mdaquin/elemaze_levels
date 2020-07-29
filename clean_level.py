import json
import copy
import math
import sys


level = {}
with open(sys.argv[1]) as f:
    level = json.load(f)


def display(level):
    strr = ''
    for i in range(0, len(level["matrix"])):
        row = level["matrix"][len(level["matrix"])-1-i]
        for cell in row:
            if cell["color"] == "x":
                strr+="     "
            elif 1 not in cell["ydirs"]:
                strr+='_____'
            else:
                strr+='     '
        strr+='\n'
        for x in range(0,3):                        
            for j,cell in enumerate(row):
                m = cell['color']
                if level["chest_position"]["y"] == len(level["matrix"])-1-i and level["chest_position"]["x"] == j: m= "C"
                if level["fireman_position"]["y"] == len(level["matrix"])-1-i and level["fireman_position"]["x"] == j: m= "F"
                if level["airman_position"]["y"] == len(level["matrix"])-1-i and level["airman_position"]["x"] == j: m= "A"
                if level["earthman_position"]["y"] == len(level["matrix"])-1-i and level["earthman_position"]["x"] == j: m= "E"
                if level["waterman_position"]["y"] == len(level["matrix"])-1-i and level["waterman_position"]["x"] == j: m= "W" 
                if -1 not in cell['xdirs'] and m!='x': strr+='|'
                else: strr+=' '
                if cell["color"] == "x":
                    strr+="   "
                else:
                    strr+=cell['color']+m+cell['color']
                if 1 not in cell['xdirs'] and m!='x': strr+='|'
                else: strr+=' '            
            strr+='\n'
        for cell in row:
            if cell['color'] == "x":
                strr+="     "
            elif -1 not in cell["ydirs"]:
                strr+='_____'
            else:
                strr+='     '
        strr+='\n'
        
    print(strr)



nlevel = {}

mini = 11
minj = 11
maxi = -1
maxj = -1
for i, row in enumerate(level["matrix"]):
    for j, cell in enumerate(row):
        if cell["color"] != "x":
            if i < mini: mini = i
            if i > maxi: maxi = i
            if j < minj: minj = j
            if j > maxj: maxj = j

nlevel["matrix"]=[]
for i, row in enumerate(level["matrix"]):
    if i >= mini and i <= maxi:
        nlevel["matrix"].append([])
        for j, cell in enumerate(row):
            if j >= minj and j <= maxj:
                nlevel["matrix"][i-mini].append(level["matrix"][i][j])


if level["chest_position"]["x"] == 0 and level["chest_position"]["y"] == 0:
    nlevel["chest_position"] = {"x": -1, "y": -1}
else:
    nlevel["chest_position"] = {"x": level["chest_position"]["x"]-minj, "y": level["chest_position"]["y"]-mini} 

if level["fireman_position"]["x"] == 0 and level["fireman_position"]["y"] == 0:
    nlevel["fireman_position"] = {"x": -1, "y": -1}
else:
    nlevel["fireman_position"] = {"x": level["fireman_position"]["x"]-minj, "y": level["fireman_position"]["y"]-mini} 


if level["airman_position"]["x"] == 0 and level["airman_position"]["y"] == 0:
    nlevel["airman_position"] = {"x": -1, "y": -1}
else:
    nlevel["airman_position"] = {"x": level["airman_position"]["x"]-minj, "y": level["airman_position"]["y"]-mini} 

if level["earthman_position"]["x"] == 0 and level["earthman_position"]["y"] == 0:
    nlevel["earthman_position"] = {"x": -1, "y": -1}
else:
    nlevel["earthman_position"] = {"x": level["earthman_position"]["x"]-minj, "y": level["earthman_position"]["y"]-mini} 

if level["waterman_position"]["x"] == 0 and level["waterman_position"]["y"] == 0:
    nlevel["waterman_position"] = {"x": -1, "y": -1}
else:
    nlevel["waterman_position"] = {"x": level["waterman_position"]["x"]-minj, "y": level["waterman_position"]["y"]-mini} 
                
            
display(level)
display(nlevel)

with open(sys.argv[1]+".clean", "w") as f:
    json.dump(nlevel,f)

