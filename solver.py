import json
import copy
import math
import sys
    
def contains(l,c):
    for i in l:
        if i["x"]==c["x"] and i["y"]==c["y"]: return True
    return False


def scontains(l,s):
    for ss in l:
        if s["waterman_position"]["x"]!=ss["waterman_position"]["x"]: continue
        if s["waterman_position"]["y"]!=ss["waterman_position"]["y"]: continue
        if s["airman_position"]["x"]!=ss["airman_position"]["x"]: continue
        if s["airman_position"]["y"]!=ss["airman_position"]["y"]: continue
        if s["fireman_position"]["x"]!=ss["fireman_position"]["x"]: continue
        if s["fireman_position"]["y"]!=ss["fireman_position"]["y"]: continue
        if s["earthman_position"]["x"]!=ss["earthman_position"]["x"]: continue
        if s["earthman_position"]["y"]!=ss["earthman_position"]["y"]: continue                   
        if ss["matrix"] == [] and s["matrix"] == []: return True
        elif ss["matrix"] == []: continue
        elif s["matrix"] == []: continue
        same = True
        for i in range(0, len(ss["matrix"])):
            for j in range(0, len(ss["matrix"][i])):
                if ss["matrix"][i][j]["color"] != s["matrix"][i][j]["color"]:
                    same = False
                    break
            if not same: break
        if same: return True
    return False

# implement best first search
# as in the game
def path(state, guy, dest):
    origin = state[guy+"_position"]
    toinspect = [origin]
    inspected = []
    while len(toinspect)!=0:
        item = toinspect.pop(0)
        inspected.append(item)
        if item["x"]==dest["x"] and item["y"]==dest["y"]:
            path = []
            while "parent" in item:
                path.insert(0, {"x": item["x"], "y": item["y"]})
                item = item["parent"]
            return path
        # print(str(item["y"])+" "+str(item["x"]))
        for xd in state["matrix"][item["y"]][item["x"]]["xdirs"]:
            nitem = {"x": item["x"]+xd, "y":item["y"], "parent": item}
            if item["x"]+xd >= 0 and item["x"]+xd<10 and not contains(toinspect, nitem) and not contains(inspected, nitem):
                toinspect.append(nitem)
        for yd in state["matrix"][item["y"]][item["x"]]["ydirs"]:
            nitem = {"x": item["x"], "y":item["y"]+yd, "parent": item}
            if item["y"]+yd >= 0 and item["y"]+yd < 6 and not contains(toinspect, nitem) and not contains(inspected, nitem):
                toinspect.append(nitem)                
    return {}


def runpath(state, guy, path):
    nstate = copy.deepcopy(state)
    for s in path:
        nstate[guy+"_position"] = s
        if guy=="waterman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "a":
                nstate["state"] = "gameover"
                nstate["matrix"] = []
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "f":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "w"
                if nstate["fireman_position"]["x"] == s["x"] and nstate["fireman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    nstate["matrix"] = []
                    return nstate                                    
        if guy=="earthman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "f":
                nstate["state"] = "gameover"
                nstate["matrix"] = []
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "w":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "e"
                if nstate["airman_position"]["x"] == s["x"] and nstate["airman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    nstate["matrix"] = []
                    return nstate                                    
        if guy=="fireman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "w":
                nstate["state"] = "gameover"
                nstate["matrix"] = []
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "e":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "f"
                if nstate["earthman_position"]["x"] == s["x"] and nstate["earthman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    nstate["matrix"] = []
                    return nstate                    
        if guy=="airman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "e":
                nstate["state"] = "gameover"
                nstate["matrix"] = []
                return nstate
        if s["x"] == nstate["chest_position"]["x"] and s["y"] == nstate["chest_position"]["y"]:
            nstate["state"] = "win"
            return nstate
    return nstate
            

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


# breath first search solver - inefficient
def bfs_solve(root):
    toinspect = [root]
    inspected = []
    while len(toinspect) != 0:
        # print(str(len(toinspect))+"/"+str(len(inspected)))
        state = toinspect.pop(0)        
        inspected.append(state)
        if "state" in state and state["state"] == "gameover":
            continue
        elif "state" in state and state["state"] == "win":
            print("solved inspecting "+str(len(inspected))+" states ("+str(len(toinspect))+")")
            return state
        for i in range(0, len(state["matrix"])):
            for j in range(0, len(state["matrix"][i])):
                if not (state["fireman_position"]["y"] == i and state["fireman_position"]["x"] == j) and not (state["earthman_position"]["y"] == i and state["earthman_position"]["x"] == j) and not (state["waterman_position"]["y"] == i and state["waterman_position"]["x"] == j) and not (state["airman_position"]["y"] == i and state["airman_position"]["x"] == j) and not state["matrix"][i][j] == "x":
                    if state["airman_position"]["x"] != -1:
                        p = path(state, "airman", {"x": j, "y": i})                        
                        nstate = runpath(state, "airman", p)
                        nstate["parent"] = state
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["waterman_position"]["x"] != -1:
                        p = path(state, "waterman", {"x": j, "y": i})
                        nstate = runpath(state, "waterman", p)
                        nstate["parent"] = state                        
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["fireman_position"]["x"] != -1:
                        p=path(state, "fireman", {"x": j, "y": i})
                        nstate = runpath(state, "fireman", p)
                        nstate["parent"] = state                        
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["earthman_position"]["x"] != -1:
                        p = path(state, "earthman", {"x": j, "y": i})
                        nstate = runpath(state, "earthman", p)
                        nstate["parent"] = state                        
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
    return {}

def distance(p1, p2):
    return math.sqrt(((p2["x"]-p1["x"])**2.0)+((p2["y"]-p1["y"])**2.0))

# append at right place according to score
def sappend(si, l):
    for i,se in enumerate(l):
        if se["score"]>si["score"]:
            l.insert(i, si)
            return 
    l.append(si)
    
# A* solver - should be more efficient
def astar_solve(root):
    root["steps"] = 0
    root["distance"] = min(distance(root["chest_position"], root["fireman_position"]),
                           distance(root["chest_position"], root["airman_position"]),
                           distance(root["chest_position"], root["earthman_position"]),
                           distance(root["chest_position"], root["waterman_position"]))
    root["score"] = root["steps"]+root["distance"]
    toinspect = [root] # should be ordered by score
    inspected = []
    while len(toinspect) != 0:
        # print(str(len(toinspect))+"/"+str(len(inspected)))
        state = toinspect.pop(0)        
        inspected.append(state)
        if "state" in state and state["state"] == "gameover":
            continue
        elif "state" in state and state["state"] == "win":
            print("solved inspecting "+str(len(inspected))+" states ("+str(len(toinspect))+")")
            print("score::"+str(state["score"]))
            print("score of parent::"+str(state["parent"]["score"]))    
            return state
        for i in range(0, len(state["matrix"])):
            for j in range(0, len(state["matrix"][i])):
                if not (state["fireman_position"]["y"] == i and state["fireman_position"]["x"] == j) and not (state["earthman_position"]["y"] == i and state["earthman_position"]["x"] == j) and not (state["waterman_position"]["y"] == i and state["waterman_position"]["x"] == j) and not (state["airman_position"]["y"] == i and state["airman_position"]["x"] == j) and not state["matrix"][i][j] == "x":
                    if state["airman_position"]["x"] != -1:
                        p = path(state, "airman", {"x": j, "y": i})                        
                        nstate = runpath(state, "airman", p)
                        nstate["parent"] = state
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            nstate["steps"] = state["steps"]+1
                            nstate["distance"] = min(distance(nstate["chest_position"], nstate["fireman_position"]),
                                                   distance(nstate["chest_position"], nstate["airman_position"]),
                                                   distance(nstate["chest_position"], nstate["earthman_position"]),
                                                   distance(nstate["chest_position"], nstate["waterman_position"]))
                            nstate["score"] = nstate["steps"]+nstate["distance"]
                            sappend(nstate, toinspect)
                    if state["waterman_position"]["x"] != -1:
                        p = path(state, "waterman", {"x": j, "y": i})
                        nstate = runpath(state, "waterman", p)
                        nstate["parent"] = state             
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            nstate["steps"] = state["steps"]+1
                            nstate["distance"] = min(distance(nstate["chest_position"], nstate["fireman_position"]),
                                                   distance(nstate["chest_position"], nstate["airman_position"]),
                                                   distance(nstate["chest_position"], nstate["earthman_position"]),
                                                   distance(nstate["chest_position"], nstate["waterman_position"]))
                            nstate["score"] = nstate["steps"]+nstate["distance"]
                            sappend(nstate, toinspect)                            
                    if state["fireman_position"]["x"] != -1:
                        p=path(state, "fireman", {"x": j, "y": i})
                        nstate = runpath(state, "fireman", p)
                        nstate["parent"] = state                        
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            nstate["steps"] = state["steps"]+1
                            nstate["distance"] = min(distance(nstate["chest_position"], nstate["fireman_position"]),
                                                   distance(nstate["chest_position"], nstate["airman_position"]),
                                                   distance(nstate["chest_position"], nstate["earthman_position"]),
                                                   distance(nstate["chest_position"], nstate["waterman_position"]))
                            nstate["score"] = nstate["steps"]+nstate["distance"]
                            sappend(nstate, toinspect)     
                    if state["earthman_position"]["x"] != -1:
                        p = path(state, "earthman", {"x": j, "y": i})
                        nstate = runpath(state, "earthman", p)
                        nstate["parent"] = state                        
                        # display(nstate)
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            nstate["steps"] = state["steps"]+1
                            nstate["distance"] = min(distance(nstate["chest_position"], nstate["fireman_position"]),
                                                   distance(nstate["chest_position"], nstate["airman_position"]),
                                                   distance(nstate["chest_position"], nstate["earthman_position"]),
                                                   distance(nstate["chest_position"], nstate["waterman_position"]))
                            nstate["score"] = nstate["steps"]+nstate["distance"]
                            sappend(nstate, toinspect) 
    return {}



if __name__ == '__main__':
    level = {}
    with open(sys.argv[1]) as f:
        level = json.load(f)
        
    algo="astar"
    if len(sys.argv) == 3:
        algo=sys.argv[2]
    
    display(level)

    if algo == "bfs":
        print("solving with Breadth First Search")
        solution = bfs_solve(level)
    elif algo== "display":
        sys.exit()
    else:
        print("solving with A*")    
        solution = astar_solve(level)

    asol = [solution]
    while "parent" in solution:
        asol.insert(0,solution["parent"])
        solution=solution["parent"]

    print("===== SOLUTION ("+str(len(asol))+" steps) =====")
    
    for s in asol:
        display(s)

