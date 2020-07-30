import config
import random
import solver
import os
import json
import math 
# fitness:
#    - distance to the ideal number of steps of the solution
#    - compactness of the level
#    - use to the guys (ration of the guys present that are moving)

def generate_cell():
    # each color is equally possible
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
    if random.random() < config.p_g_dir:
        cell["ydirs"].append(1)
    if random.random() > config.p_g_dir:
        cell["ydirs"].append(-1)
    cell["xdirs"] = []
    if random.random() > config.p_g_dir:
        cell["xdirs"].append(1)
    if random.random() > config.p_g_dir:
        cell["xdirs"].append(-1)
    return cell
        
def generate_random():
    level = {}
    # TOFIX: some guys might endup on the same place
    level["chest_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    if random.random()< config.p_g_guy:
        level["fireman_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    else:
        level["fireman_position"] = {"x": -1, "y": -1}
    if random.random()< config.p_g_guy:
        level["waterman_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    else:
        level["waterman_position"] = {"x": -1, "y": -1}
    if random.random()< config.p_g_guy:
        level["airman_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    else:
        level["airman_position"] = {"x": -1, "y": -1}    
    if random.random()< config.p_g_guy:
        level["earthman_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    else:
        level["earthman_position"] = {"x": -1, "y": -1}
    level["matrix"] = []
    for i in range(0,6):
        level["matrix"].append([])
        for j in range(0,10):
            if random.random()<config.p_g_cell:
                level["matrix"][i].append(generate_cell())
            else:
                level["matrix"][i].append({"color": "x", "xdirs": [], "ydirs": []})                
    return level

def save(g,n):
    os.mkdir("results/g"+str(n))
    count = 0
    count_with_sol = 0
    sum_steps = 0
    max_steps = 0
    min_steps = 10000
    avg_fitness = 0
    max_fitness = 0
    avg_compactness = 0
    max_compactness = 0
    for gg in g:
        with open("results/g"+str(n)+"/i"+str(count)+".json", "w") as f:
            json.dump(gg,f)
        count = count +1
        if gg["nb_steps"] != 0:
            count_with_sol = count_with_sol + 1
            sum_steps = sum_steps + gg["nb_steps"]
            if gg["nb_steps"] > max_steps: max_steps = gg["nb_steps"]
            if gg["nb_steps"] < min_steps: min_steps = gg["nb_steps"]
        avg_fitness = avg_fitness + gg["fitness"]
        if gg["fitness"] > max_fitness: max_fitness = gg["fitness"]
        avg_compactness = avg_compactness + gg["compactness"]
        if gg["compactness"] > max_compactness: max_compactness = gg["compactness"]
    if count_with_sol == 0: count_with_sol = 1
    with open("results/g"+str(n)+"/stats.json", "w") as f:
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
    for gg in g:
        solution = solver.astar_solve(gg)
        if "matrix" not in solution:
            gg["nb_steps"] = 0
        else:            
            asol = [solution]
            while "parent" in solution:
                asol.insert(0,solution["parent"])
                solution=solution["parent"]
            gg["nb_steps"] = len(asol)
            print("solution with "+str(gg["nb_steps"]))
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
        gg["compactness"]=1.0-((float(maxi-mini)/6.0)*(float(maxj-minj)/10.0))
        gg["fitness"] = 1+config.wsolution*(min(float(config.idealsol), float(gg["nb_steps"]))/max(float(config.idealsol), float(gg["nb_steps"])))+config.wsize*gg["compactness"]
    # moving guy 

def mutate(gg):
    # mutate position of guy
    if random.random() < 0.5:
        r = random.random()
        if r < 0.20:
            # TOFIX: only put it where there is something
            gg["fireman_position"] = {"x": random.randint(-1,9), "y": random.randint(0,5)}
        elif r < 0.40:
            gg["airman_position"] = {"x": random.randint(-1,9), "y": random.randint(0,5)}
        elif r < 0.60:
            gg["earthman_position"] = {"x": random.randint(-1,9), "y": random.randint(0,5)}
        elif r < 0.80:
            gg["waterman_position"] = {"x": random.randint(-1,9), "y": random.randint(0,5)}
        else:
            gg["chest_position"] = {"x": random.randint(0,9), "y": random.randint(0,5)}
    else:
        i = random.randint(0,5)
        j = random.randint(0,9)
        gg["matrix"][i][j] = generate_cell()
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
        ng.append(g[selected])
    for i,gg in enumerate(ng):
        if random.random() < config.mut_rate:
            ng[i] = mutate(gg)
    # crossover
    return ng


g0 = []

for i in range(0, config.g_size):
    l = generate_random()
    g0.append(l)

g = g0
generations = 0
while generations <= config.g_num:
    print("generation "+str(generations))
    assess(g)
    save(g, generations)
    g = newgeneration(g)
    generations = generations+1


    

