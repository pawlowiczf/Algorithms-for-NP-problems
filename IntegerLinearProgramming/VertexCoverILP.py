from dimacs import *
from multiprocessing import Process
from pulp import *
import os 


def VertexCoverILP2(G, E):
    n = len(G)

    variablesMap = {} 
    objectiveFunc = 0 

    model = LpProblem("VertexCover", LpMinimize)

    for a in range(n):
        label = f'x_{a}'

        v = LpVariable(name=label, lowBound=0, upBound=1, cat=LpBinary)
        variablesMap[label] = v 
        
        objectiveFunc += v 
    #
    
    for (a, b) in E:
        labelA, labelB = f'x_{a}', f'x_{b}' 
        vA, vB = variablesMap[labelA], variablesMap[labelB] 
        model += vA + vB >= 1 
    #

    model += objectiveFunc
    return model 
#

def VertexCoverILP(G, E):
    n = len(G)
    model = LpProblem("VertexCover", LpMinimize)

    variables = [LpVariable(f"x_{i}", cat="Binary") for i in range(n)]

    model += lpSum(variables)

    for a, b in E:
        model += variables[a] + variables[b] >= 1

    return model
#

def RunILPParralel(G, E):
    #
    n = len(G)

    model = VertexCoverILP(G, E) 
    model.solve(PULP_CBC_CMD(msg=False))

    if model.status == 1:
        print(f'Success. {value(model.objective)} - {n}')
    else:
        print('Failure. Not found. Error')

# end procedure 

path = "./graph/"
files = [entry.name for entry in os.scandir(path) if entry.is_file()]
def main():
    #
    counter, numberOfTests = 1, len(files)

    for name in files:
        print(f"{counter}/{numberOfTests}: {name}")

        G = loadGraph(f'{path}{name}')
        E = edgeList(G)

        p = Process(target=RunILPParralel, args=(G, E))
        p.start()
        p.join(timeout=3)
        if p.is_alive():
            p.terminate()
            p.join()
            print("\033[93mTime limit exceeded\033[0m")
        #
        
        counter += 1
    # end 'for' loop 

# end procedure main()
if __name__ == '__main__':
    main() 