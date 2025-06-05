from dimacs import *
import os 
import pycosat 
from multiprocessing import Process

def index( i, j ):
  return int( (i + j) * ( i + j + 1 ) / 2 + i + 1)
#

def ThresholdFunctionFormula(G, E):
    n = len(G) 
    formula = []

    for i in range(1, n + 1):
        formula.append( [index(i, 0)] )
    #
    for j in range(1, n + 1):
        formula.append( [-index(0, j)] )
    #

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            formula.append( [-index(i - 1, j), index(i, j)] )
            formula.append( [-index(i - 1, j - 1 ), -i, index(i, j)] )
    #

    return formula 
#

def VertexCoverToSAT(G, E):
    formula = [] 

    for (a, b) in E: 
        formula.append( [a + 1, b + 1] )
    #

    return formula 
#

def RunPycoSATParralel(G, E):
    #
    n = len(G)

    formulaB = ThresholdFunctionFormula(G, E) 

    k = 2
    while k <= n:
        formulaA = VertexCoverToSAT(G, E)
        formulaB.append( [-index(n, k + 1)] )

        formulaResults = pycosat.solve(formulaA + formulaB)

        if formulaResults == 'UNSAT': k += 1
        else: 
            print(f'Success: {k} - {n}')
            return 

        formulaB.pop()
    # end 'while' loop  

    print('Failure. Not found.')

    # result = CheckColoring(G, k, coloring)
    # if result: 
    #     print("GOOD", flush=True)
    # else:
    #     print("WRONG", flush=True)
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

        p = Process(target=RunPycoSATParralel, args=(G, E))
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