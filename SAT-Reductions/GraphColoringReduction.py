import os 
import pycosat     
from dimacs import loadX3CWithSolution, loadGraph, edgeList
from multiprocessing import Process

path = "./graphs-colorings/"
files = [entry.name for entry in os.scandir(path) if entry.is_file()]
# files = files[:10]

# kodowanie zmiennej do SAT:
# x_ij = i * k + j, gdzie:
# i - numer wierzchołka [0, n - 1], k - liczba kolorów, j - numer koloru [1, k]
def ReductionColoringToSAT(G, E, k):
    n = len(G)
    formula = [] 

    for v in range(n):
        base = v * k 
        clause = [base + j for j in range(1, k + 1)]
        formula.append(clause)

        for k1 in range(1, k + 1):
            for k2 in range(k1 + 1, k + 1):
                clause = [-(base + k1), -(base + k2)]
                formula.append(clause)
        #
    # end 'for' loops

    for (u, v) in E:
        for k1 in range(1, k + 1):
            clause = [-(u * k + k1), -(v * k + k1)]
            formula.append(clause)
    # end 'for' loops 

    return formula 
# end procedure

def RunParralel(G, E):
    #
    k = 2
    coloring = []
    while True:
        formula = ReductionColoringToSAT(G, E, k)
        coloring = pycosat.solve(formula)

        if coloring == 'UNSAT': k += 1
        else: break 
    # end 'while' loop  

    result = CheckColoring(G, k, coloring)
    if result: 
        print("GOOD", flush=True)
    else:
        print("WRONG", flush=True)
# end procedure 

def main():
    #
    counter, numberOfTests = 1, len(files)

    for name in files:
        print(f"{counter}/{numberOfTests}: {name}")

        G = loadGraph(f'{path}{name}')
        E = edgeList(G)

        p = Process(target=RunParralel, args=(G, E))
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

from collections import deque 

def BFS(G, C, V, vertex):
    V[vertex] = True 
    queue = deque()
    queue.appendleft(vertex)

    while queue:
        vertex = queue.popleft()
        for neighbour in G[vertex]:
            if C[neighbour] == C[vertex]: 
                return False 
            if V[neighbour] == False:
                V[neighbour] = True 
                queue.appendleft(neighbour)
        #
    #

    return True 
#

def DecodeColoring(coloring, n, k):
    decoder = []

    for var in coloring:
        if var > 0: 
            i = (var - 1) // k  # Indeks wierzchołka
            j = var - i * k  # Kolor (od 1 do k)
            decoder.append(j)  # Przypisanie koloru wierzchołkowi
    #
    return decoder
#

def CheckColoring(G, k, coloring):
    n = len(G)
    V = [False for _ in range(n)]
    C = DecodeColoring(coloring, n, k)

    flag = True 

    for v in range(n):
        if V[v] == False:
            flag = flag and BFS(G, C, V, v)
    #

    return flag
# end procedure CheckColoring()

if __name__ == '__main__':
    main()