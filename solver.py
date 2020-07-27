import json
import copy

level = {}
with open("samples/example_level.json") as f:
    level = json.load(f)


def contains(l,c):
    for i in l:
        if i["x"]==c["x"] and i["y"]==c["y"]: return True
    return False


def scontains(l,s):
    for ss in l:
        if s["waterman_position"]["x"]!=ss["waterman_position"]["x"]: break
        if s["waterman_position"]["y"]!=ss["waterman_position"]["y"]: break
        if s["airman_position"]["x"]!=ss["airman_position"]["x"]: break
        if s["airman_position"]["y"]!=ss["airman_position"]["y"]: break
        if s["fireman_position"]["x"]!=ss["fireman_position"]["x"]: break
        if s["fireman_position"]["y"]!=ss["fireman_position"]["y"]: break
        if s["earthman_position"]["x"]!=ss["earthman_position"]["x"]: break
        if s["earthman_position"]["y"]!=ss["earthman_position"]["y"]: break                   
        same = true
        for i in range(0, len(ss["matrix"])):
            for j in range(0, len(ss["matrix"][i])):
                if ss["matrix"][i][j]["color"] != s["matrix"][i][j]["color"]:
                    same = false
                    break
            if not same: break
        if same: return true
    return false

# implement best first search
# as in the game
def path(state, guy, dest):
    origin = state[guy+"_position"]
    toinspect = [origin]
    inspected = []
    while len(toinspect)!=0:
        item = toinspect.pop(0)
        if item["x"]==dest["x"] and item["y"]==dest["y"]:
            path = []
            while "parent" in item:
                path.insert(0, {"x": item["x"], "y": item["y"]})
                item = item["parent"]
            return path
        for xd in state["matrix"][item["y"]][item["x"]]["xdirs"]:
            nitem = {"x": item["x"]+xd, "y":item["y"], "parent": item}
            if not contains(toinspect, nitem) and not contains(inspected, nitem):
                toinspect.append(nitem)
        for yd in state["matrix"][item["y"]][item["x"]]["ydirs"]:
            nitem = {"x": item["x"], "y":item["y"]+yd, "parent": item}
            if not contains(toinspect, nitem) and not contains(inspected, nitem):
                toinspect.append(nitem)
    return {}


def runpath(state, guy, path):
    nstate = copy.deepcopy(state)
    for s in path:
        nstate[guy+"_position"] = s
        if guy=="waterman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "a":
                nstate["state"] = "gameover"                
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "f":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "w"
                if nstate["fireman_position"]["x"] == s["x"] and nstate["fireman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    return nstate                                    
        if guy=="earthman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "f":
                nstate["state"] = "gameover"
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "w":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "e"
                if nstate["airman_position"]["x"] == s["x"] and nstate["airman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    return nstate                                    
        if guy=="fireman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "w":
                nstate["state"] = "gameover"
                return nstate
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "e":
                nstate["matrix"][s["y"]][s["x"]]["color"] = "f"
                if nstate["earthman_position"]["x"] == s["x"] and nstate["earthman_position"]["y"] == s["y"]:
                    nstate["state"] = "gameover"
                    return nstate                    
        if guy=="airman":
            if nstate["matrix"][s["y"]][s["x"]]["color"] == "e":
                nstate["state"] = "gameover"
                return nstate
        display(nstate)
    return nstate
            

def display(level):
    strr = ''
    for i in range(0, len(level["matrix"])):
        row = level["matrix"][len(level["matrix"])-1-i]
        for cell in row:
            if 1 not in cell["ydirs"]:
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
                if -1 not in cell['xdirs']: strr+='|'
                else: strr+=' '
                strr+=cell['color']+m+cell['color']
                if 1 not in cell['xdirs']: strr+='|'
                else: strr+=' '            
            strr+='\n'
        for cell in row:
            if -1 not in cell["ydirs"]:
                strr+='_____'
            else:
                strr+='     '
        strr+='\n'
        
    print(strr)


# breath first search first.
# if too slow, will move to A*
def solve(root):
    toinspect = [root]
    inspected = []
    while len(toinspect) != 0:
        print(str(len(toinspect))+"/"+str(len(inspected)))
        state = toinspect.pop(0)
        if "state" in state and state["state"] == "gameover":
            break
        elif "state" in state and state["state"] == "win":
            return state
        for i in range(0, len(state["matrix"])):
            for j in range(0, len(state["matrix"][i])):
                if not (state["fireman_position"]["y"] == i and state["fireman_position"]["x"] == j) and not (state["earthman_position"]["y"] == i and state["earthman_position"]["x"] == j) and not (state["waterman_position"]["y"] == i and state["waterman_position"]["x"] == j) and not (state["airman_position"]["y"] == i and state["airman_position"]["x"] == j):
                    if state["airman_position"]["x"] != -1:
                        nstate = runpath(state, "airman", path(state, "airman", {"x": i, "y": j}))
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["waterman_position"]["x"] != -1:
                        nstate = runpath(state, "airman", path(state, "airman", {"x": i, "y": j}))
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["fireman_position"]["x"] != -1:
                        nstate = runpath(state, "airman", path(state, "airman", {"x": i, "y": j}))
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
                    if state["earthman_position"]["x"] != -1:
                        nstate = runpath(state, "airman", path(state, "airman", {"x": i, "y": j}))
                        if not scontains(toinspect, nstate) and not scontains(inspected, nstate):
                            toinspect.append(nstate)
    return {}
                       
# display(level)

solve(level)
