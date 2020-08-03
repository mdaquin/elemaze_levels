import config
import random
import solver
import os
import json
import math 
import copy
import sys

# TOFIX crossover
# TODO: add in fitness something about movement freedom, e.g. the average number non-empty places reachable by the guys
# TOFIX implement elitism... 
# TOFIX compactness is wrong
# TODO: cross generation stats
# TODO: more incremental moves for guys
# TOFIX: change the color when putting a guy originally
# TOTEST: only put guys on places that don't kill them
def generate_cell(matrix, i, j):
    # TOFIX: sometimes we might get 4 walls...
    cell = {}
    r_color = random.random()
    if r_color < 0.25:
        cell["color"] = "f"
    elif r_color < 0.5:
        cell["color"] = "a"
    elif r_color < 0.75:
        cell["color"] = "e"    
    else:
        cell["color"] = "w"
    cell["ydirs"] = []    
    if i!=config.maxy-1 and random.random() < config.p_g_dir:
        cell["ydirs"].append(1)
    if i != 0 and matrix[i-1][j]["color"] != "x" and 1 in matrix[i-1][j]["ydirs"]:
        cell["ydirs"].append(-1)
    cell["xdirs"] = []
    if j!=config.maxx-1 and random.random() > config.p_g_dir:
        cell["xdirs"].append(1)
    if j != 0 and matrix[i][j-1]["color"] != "x" and 1 in matrix[i][j-1]["xdirs"]:        
        cell["xdirs"].append(-1)
    return cell
        
def generate_random():
    level = {}
    level["matrix"] = []
    for i in range(0,config.maxy):
        level["matrix"].append([])
        for j in range(0,config.maxx):
            if random.random()<config.p_g_cell:
                level["matrix"][i].append(generate_cell(level["matrix"], i, j))
            else:
                level["matrix"][i].append({"color": "x", "xdirs": [], "ydirs": []})
                if i!=0 and 1 in level["matrix"][i-1][j]["ydirs"]:
                    level["matrix"][i-1][j]["ydirs"].pop(level["matrix"][i-1][j]["ydirs"].index(1))
                if j!=0 and 1 in level["matrix"][i][j-1]["xdirs"]:
                    level["matrix"][i][j-1]["xdirs"].pop(level["matrix"][i][j-1]["xdirs"].index(1))
                    
    found = False
    while not found:
        level["chest_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
        if level["matrix"][level["chest_position"]["x"]][level["chest_position"]["y"]]["color"] != "x":
            found=True
        
    if random.random()< config.p_g_guy:

        found = False
        while not found:
            level["fireman_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
            if level["matrix"][level["fireman_position"]["x"]][level["fireman_position"]["y"]]["color"] != "x" and level["matrix"][level["fireman_position"]["x"]][level["fireman_position"]["y"]]["color"] != "w" and not (level["fireman_position"]["x"] == level["chest_position"]["x"] and level["fireman_position"]["y"] == level["chest_position"]["y"]):
                found=True
                    
    else:
        level["fireman_position"] = {"x": -1, "y": -1}
    if random.random()< config.p_g_guy:
        found = False
        while not found:
            level["waterman_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
            if level["matrix"][level["waterman_position"]["x"]][level["waterman_position"]["y"]]["color"] != "x" and level["matrix"][level["waterman_position"]["x"]][level["fireman_position"]["y"]]["color"] != "a" and not (level["waterman_position"]["x"] == level["chest_position"]["x"] and level["waterman_position"]["y"] == level["chest_position"]["y"]) and not (level["waterman_position"]["x"] == level["fireman_position"]["x"] and level["waterman_position"]["y"] == level["fireman_position"]["y"]):
                found=True
                
    else:
        level["waterman_position"] = {"x": -1, "y": -1}
    if random.random()< config.p_g_guy:
        found = False
        while not found:
            level["airman_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
            if level["matrix"][level["airman_position"]["x"]][level["airman_position"]["y"]]["color"] != "x" and level["matrix"][level["airman_position"]["x"]][level["fireman_position"]["y"]]["color"] != "e" and not (level["airman_position"]["x"] == level["chest_position"]["x"] and level["airman_position"]["y"] == level["chest_position"]["y"]) and not (level["airman_position"]["x"] == level["fireman_position"]["x"] and level["airman_position"]["y"] == level["fireman_position"]["y"]) and not (level["airman_position"]["x"] == level["waterman_position"]["x"] and level["airman_position"]["y"] == level["waterman_position"]["y"]):
                found=True
                
    else:
        level["airman_position"] = {"x": -1, "y": -1}    
    if random.random()< config.p_g_guy:
        found = False
        while not found:
            level["earthman_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
            if level["matrix"][level["earthman_position"]["x"]][level["earthman_position"]["y"]]["color"] != "x" and level["matrix"][level["earthman_position"]["x"]][level["earthman_position"]["y"]]["color"] != "f" and not (level["earthman_position"]["x"] == level["chest_position"]["x"] and level["earthman_position"]["y"] == level["chest_position"]["y"]) and not (level["earthman_position"]["x"] == level["fireman_position"]["x"] and level["earthman_position"]["y"] == level["fireman_position"]["y"]) and not (level["earthman_position"]["x"] == level["waterman_position"]["x"] and level["earthman_position"]["y"] == level["waterman_position"]["y"]) and not (level["earthman_position"]["x"] == level["airman_position"]["x"] and level["earthman_position"]["y"] == level["airman_position"]["y"]):
                found=True
    else:
        level["earthman_position"] = {"x": -1, "y": -1}
    return level

def save(g,n):
    os.mkdir(result_folder+"/g"+str(n))
    count = 0
    count_with_sol = 0
    sum_steps = 0
    max_steps = 0
    min_steps = 10000
    avg_fitness = 0
    max_fitness = 0
    max_fitnessgg = {}
    max_fitnessi = 0    
    avg_compactness = 0
    max_compactness = 0    
    for i, gg in enumerate(g):
        with open(result_folder+"/g"+str(n)+"/i"+str(count)+".json", "w") as f:
            json.dump(gg,f)
        count = count +1
        if gg["nb_steps"] != 0:
            count_with_sol = count_with_sol + 1
            sum_steps = sum_steps + gg["nb_steps"]
            if gg["nb_steps"] > max_steps: max_steps = gg["nb_steps"]
            if gg["nb_steps"] < min_steps: min_steps = gg["nb_steps"]
        avg_fitness = avg_fitness + gg["fitness"]
        if gg["fitness"] > max_fitness:
            max_fitness = gg["fitness"]
            max_fitnessgg = gg
            max_fitnessi = i
        avg_compactness = avg_compactness + gg["compactness"]
        if gg["compactness"] > max_compactness: max_compactness = gg["compactness"]
    if count_with_sol == 0: count_with_sol = 1
    print("=== best in generation ("+str(max_fitnessi)+")===")
    solver.display(max_fitnessgg)
    with open(result_folder+"/g"+str(n)+"/stats.json", "w") as f:
        json.dump({"count_with_sol": count_with_sol,
                   "avg_steps": sum_steps/count_with_sol,
                   "max_steps": max_steps,
                   "min_steps": min_steps,
                   "avg_fitness": avg_fitness/count,
                   "max_ftitness": max_fitness,
                   "avg_compactness": avg_compactness/count,
                   "max_compactness": max_compactness}, f)
    print("max_fitness: "+str(max_fitness))
    print("max_steps: "+str(max_steps))
    print("max_compactness: "+str(max_compactness))

def assess(g):
    for x,gg in enumerate(g):
        if "solved" not in gg or not gg["solved"]:
            print("solving "+str(x))
            solution = solver.astar_solve(gg)
            print("done")
            if "matrix" not in solution:
                gg["nb_steps"] = 0
            else:            
                asol = [solution]
                while "parent" in solution:
                    asol.insert(0,solution["parent"])
                    solution=solution["parent"]
                gg["nb_steps"] = len(asol)
                print("solution with "+str(gg["nb_steps"]))
        gg["solved"] = True
        # compactness
        mini = 11
        minj = 11
        maxi = 0
        maxj = 0
        for i, row in enumerate(gg["matrix"]):
            for j,cell in enumerate(row):
                if cell["color"]!="x":
                    if i < mini: mini = i
                    if i > maxi: maxi = i
                    if j < minj: minj = j
                    if j > maxj: maxj = j
        gg["compactness"]=1.0-((float(maxi-mini)/float(config.maxy))*(float(maxj-minj)/float(config.maxx)))
        gg["fitness"] = config.wsolution*(min(float(config.idealsol), float(gg["nb_steps"]))/max(float(config.idealsol), float(gg["nb_steps"])))+config.wsize*gg["compactness"]
    # moving guy 

def mutate(gg):
    # mutate position of guy
    if random.random() < 0.5:
        r = random.random()
        if r < 0.20:
            found = False
            while not found:
                gg["fireman_position"] = {"x": random.randint(-1,config.maxx-1), "y": random.randint(0,config.maxy-1)}
                if gg["matrix"][gg["fireman_position"]["x"]][gg["fireman_position"]["y"]]["color"] != "x" and gg["matrix"][gg["fireman_position"]["x"]][gg["fireman_position"]["y"]]["color"] != "w" and not (gg["fireman_position"]["x"] == gg["chest_position"]["x"] and gg["fireman_position"]["y"] == gg["chest_position"]["y"]) and not (gg["fireman_position"]["x"] == gg["earthman_position"]["x"] and gg["earthman_position"]["y"] == gg["fireman_position"]["y"]) and not (gg["fireman_position"]["x"] == gg["waterman_position"]["x"] and gg["fireman_position"]["y"] == gg["waterman_position"]["y"]) and not (gg["fireman_position"]["x"] == gg["airman_position"]["x"] and gg["fireman_position"]["y"] == gg["airman_position"]["y"]):
                    found=True
        elif r < 0.40:
            found=False
            while not found:
                gg["airman_position"] = {"x": random.randint(-1,config.maxx-1), "y": random.randint(0,config.maxy-1)}
                if gg["matrix"][gg["airman_position"]["x"]][gg["airman_position"]["y"]]["color"] != "x" and gg["matrix"][gg["airman_position"]["x"]][gg["airman_position"]["y"]]["color"] != "e" and not (gg["airman_position"]["x"] == gg["chest_position"]["x"] and gg["airman_position"]["y"] == gg["chest_position"]["y"]) and not (gg["airman_position"]["x"] == gg["earthman_position"]["x"] and gg["earthman_position"]["y"] == gg["airman_position"]["y"]) and not (gg["airman_position"]["x"] == gg["waterman_position"]["x"] and gg["airman_position"]["y"] == gg["waterman_position"]["y"]) and not (gg["airman_position"]["x"] == gg["fireman_position"]["x"] and gg["airman_position"]["y"] == gg["fireman_position"]["y"]):
                    found = True
        elif r < 0.60:
            found = False
            while not found:                
                gg["earthman_position"] = {"x": random.randint(-1,config.maxx-1), "y": random.randint(0,config.maxy-1)}
                if gg["matrix"][gg["earthman_position"]["x"]][gg["earthman_position"]["y"]]["color"] != "x" and gg["matrix"][gg["earthman_position"]["x"]][gg["earthman_position"]["y"]]["color"] != "f" and not (gg["earthman_position"]["x"] == gg["chest_position"]["x"] and gg["earthman_position"]["y"] == gg["chest_position"]["y"]) and not (gg["earthman_position"]["x"] == gg["airman_position"]["x"] and gg["earthman_position"]["y"] == gg["airman_position"]["y"]) and not (gg["earthman_position"]["x"] == gg["waterman_position"]["x"] and gg["earthman_position"]["y"] == gg["waterman_position"]["y"]) and not (gg["earthman_position"]["x"] == gg["fireman_position"]["x"] and gg["earthman_position"]["y"] == gg["fireman_position"]["y"]):
                    found=True
        elif r < 0.80:
            found = False
            while not found:
                gg["waterman_position"] = {"x": random.randint(-1,config.maxx-1), "y": random.randint(0,config.maxy-1)}
                if gg["matrix"][gg["waterman_position"]["x"]][gg["waterman_position"]["y"]]["color"] != "x" and gg["matrix"][gg["waterman_position"]["x"]][gg["waterman_position"]["y"]]["color"] != "a" and not (gg["waterman_position"]["x"] == gg["chest_position"]["x"] and gg["waterman_position"]["y"] == gg["chest_position"]["y"]) and not (gg["waterman_position"]["x"] == gg["airman_position"]["x"] and gg["waterman_position"]["y"] == gg["airman_position"]["y"]) and not (gg["waterman_position"]["x"] == gg["earthman_position"]["x"] and gg["waterman_position"]["y"] == gg["earthman_position"]["y"]) and not (gg["waterman_position"]["x"] == gg["fireman_position"]["x"] and gg["waterman_position"]["y"] == gg["fireman_position"]["y"]):
                    found = True
        else:
            found = False
            while not found:
                gg["chest_position"] = {"x": random.randint(0,config.maxx-1), "y": random.randint(0,config.maxy-1)}
                if gg["matrix"][gg["chest_position"]["x"]][gg["chest_position"]["y"]]["color"] != "x" and not (gg["chest_position"]["x"] == gg["waterman_position"]["x"] and gg["chest_position"]["y"] == gg["waterman_position"]["y"]) and not (gg["chest_position"]["x"] == gg["airman_position"]["x"] and gg["chest_position"]["y"] == gg["airman_position"]["y"]) and not (gg["chest_position"]["x"] == gg["earthman_position"]["x"] and gg["chest_position"]["y"] == gg["earthman_position"]["y"]) and not (gg["chest_position"]["x"] == gg["fireman_position"]["x"] and gg["chest_position"]["y"] == gg["fireman_position"]["y"]):
                    found=True
    else:
        i = random.randint(0,config.maxy-1)
        j = random.randint(0,config.maxx-1)
        if random.random() < 0.5:
            previouscolor = gg["matrix"][i][j]["color"]
            posiblecolors = ["x","a","w","f","e"]
            posiblecolors.pop(posiblecolors.index(gg["matrix"][i][j]["color"]))
            gg["matrix"][i][j]["color"] = posiblecolors[random.randint(0,3)]
            if gg["matrix"][i][j]["color"] == "x":
                gg["matrix"][i][j]["xdirs"] = []
                gg["matrix"][i][j]["ydirs"] = []                
                if i != 0 and 1 in gg["matrix"][i-1][j]["ydirs"]:
                    gg["matrix"][i-1][j]["ydirs"].pop(gg["matrix"][i-1][j]["ydirs"].index(1))
                if i != config.maxy-1 and -1 in gg["matrix"][i+1][j]["ydirs"]:
                    gg["matrix"][i+1][j]["ydirs"].pop(gg["matrix"][i+1][j]["ydirs"].index(-1))
                if j != 0 and 1 in gg["matrix"][i][j-1]["xdirs"]:
                    gg["matrix"][i][j-1]["xdirs"].pop(gg["matrix"][i][j-1]["xdirs"].index(1))
                if j != config.maxx-1 and -1 in gg["matrix"][i][j+1]["xdirs"]:
                    gg["matrix"][i][j+1]["xdirs"].pop(gg["matrix"][i][j+1]["xdirs"].index(-1))
            if previouscolor == "x":
                gg["matrix"][i][j]["xdirs"]=[]
                gg["matrix"][i][j]["ydirs"]=[]    
        else:
            if gg["matrix"][i][j]["color"] != "x":
                r = random.random()
                if r < 0.25:
                    if 1 in gg["matrix"][i][j]["xdirs"] and j != config.maxx-1:
                        gg["matrix"][i][j]["xdirs"].pop(gg["matrix"][i][j]["xdirs"].index(1))
                        gg["matrix"][i][j+1]["xdirs"].pop(gg["matrix"][i][j+1]["xdirs"].index(-1))
                    elif j != config.maxx-1:
                        gg["matrix"][i][j]["xdirs"].append(1)
                        gg["matrix"][i][j+1]["xdirs"].append(-1)
                elif r < 0.50:
                    if -1 in gg["matrix"][i][j]["xdirs"] and j != 0:
                        gg["matrix"][i][j]["xdirs"].pop(gg["matrix"][i][j]["xdirs"].index(-1))
                        gg["matrix"][i][j-1]["xdirs"].pop(gg["matrix"][i][j-1]["xdirs"].index(1))
                    elif j != 0:
                        gg["matrix"][i][j]["xdirs"].append(-1)
                        gg["matrix"][i][j-1]["xdirs"].append(1)
                elif r < 0.75:
                    if -1 in gg["matrix"][i][j]["ydirs"] and i != 0:
                        gg["matrix"][i][j]["ydirs"].pop(gg["matrix"][i][j]["ydirs"].index(-1))
                        gg["matrix"][i-1][j]["ydirs"].pop(gg["matrix"][i-1][j]["ydirs"].index(1))
                    elif i != 0:
                        gg["matrix"][i][j]["ydirs"].append(-1)
                        gg["matrix"][i-1][j]["ydirs"].append(1)
                else:
                    if 1 in gg["matrix"][i][j]["ydirs"] and i != config.maxy-1:
                        gg["matrix"][i][j]["ydirs"].pop(gg["matrix"][i][j]["ydirs"].index(1))
                        gg["matrix"][i+1][j]["ydirs"].pop(gg["matrix"][i+1][j]["ydirs"].index(-1))
                    elif i != config.maxy-1:
                        gg["matrix"][i][j]["ydirs"].append(1)
                        gg["matrix"][i+1][j]["ydirs"].append(-1)   

    gg["solved"] = False 
    return gg
    
def newgeneration(g):
    sumfitness = 0.0
    fitnesses = []
    ng = []
    for gg in g:
        f = gg["fitness"]
        sumfitness = sumfitness + f
        fitnesses.append(f)
    print("sum fitnesses="+str(sumfitness))
    for i,f in enumerate(fitnesses):
        fitnesses[i] = f/sumfitness
    for i in range(0, config.g_size):
        cumul = 0
        r = random.random()
        selected = 0
        for j,f in enumerate(fitnesses):
            if r > cumul and r <= f+cumul:
                selected = j
                break
            cumul = cumul + f
        ng.append(copy.deepcopy(g[selected]))
    for i,gg in enumerate(ng):
        if random.random() < config.mut_rate:
            ng[i] = mutate(gg)
    # TOFIX: add crossover
    return ng

g0 = []

for i in range(0, config.g_size):
    l = generate_random()
    g0.append(l)

g = g0
generations = 0

result_folder = sys.argv[1]

while generations <= config.g_num:
    print("generation "+str(generations))
    assess(g)
    save(g, generations)
    g = newgeneration(g)
    generations = generations+1


    

