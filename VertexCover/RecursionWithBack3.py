from itertools import *
from dimacs import *

graphs = [
# ("e5"),
("e10"),
# ("e20"),
# ("e40"),
# ("e150"),
# ("s25"),
# ("s50"),
# ("s500"),
# ("b20"),
# ("b30"),
# ("b100"),
# ("k330_a"),
# ("k330_b"),
# ("k330_c"),
# ("m20"),
# ("m30"),
# ("m40"),
# ("m50"),
# ("m100"),
# ("p20"),
# ("p35"),
# ("p60"),
# ("p150"),
# ("r30_01"),
# ("r30_05"),
# ("r50_001"),
# ("r50_01"),
# ("r50_05"),
# ("r100_005"),
]

def VertexCover(G, E, k, C):
    #
    maxDegree, u = -1, -1 
    for vertex in range(len(G)):
        degree = len(G[vertex])
        if degree > maxDegree:
            maxDegree = degree 
            u = vertex 
    #
    if k == 0: return set() 
    if maxDegree == 0: return C 

    # Find a vertex 'u' with degree == 1
    for vertex in range(len(G)):
        if len(G[vertex]) == 1: 

            neighbour = next(iter(G[vertex]))
 
            newC = C.copy()
            newC.add(neighbour)

            newG = G.copy()
            for v in G[neighbour]:
                newG[v].remove(neighbour)
            newG[vertex] = set()
            newG[neighbour] = set()
            return VertexCover(newG, E, k - 1, newC) 
    #

    maxDegree, u = -1, -1 
    for vertex in range(len(G)):
        degree = len(G[vertex])
        if degree > maxDegree:
            maxDegree = degree 
            u = vertex 
    #
            
    if maxDegree == 2:
        newC = C.copy()
        newC.add(u)

        newG = G.copy()
        for neighbour in G[u]:
            newG[neighbour].discard(u)
        newG[u] = set()

        return VertexCover(newG, E, k - 1, newC)         
    elif maxDegree > 2:
        newC = C.copy()
        newC.add(u)

        newG = G.copy()
        for neighbour in G[u]:
            newG[neighbour].discard(u)
        newG[u] = set()        

        S1 = VertexCover(newG, E, k - 1, newC)
        if S1: return S1 

    return set()
#

def VertexCover2(G, E, k, C):
    #
    maxDegree, u = -1, -1 
    for vertex in range(len(G)):
        degree = len(G[vertex])
        if degree > maxDegree:
            maxDegree = degree 
            u = vertex 
    #
    if k == 0: return set() 
    if maxDegree == 0: return C 

    # Find a vertex 'u' with degree == 1
    for vertex in range(len(G)):
        if len(G[vertex]) == 1: 

            neighbour = next(iter(G[vertex]))
 
            newC = C.copy()
            newC.add(neighbour)

            newG = G.copy()
            for v in G[neighbour]:
                newG[v].remove(neighbour)
            newG[vertex] = set()
            newG[neighbour] = set()
            return VertexCover2(newG, E, k - 1, newC) 
    #

    maxDegree, u = -1, -1 
    for vertex in range(len(G)):
        degree = len(G[vertex])
        if degree > maxDegree:
            maxDegree = degree 
            u = vertex 
    #
            
    if maxDegree == 2:
        newC = C.copy()
        newC.add(u)

        newG = G.copy()
        for neighbour in G[u]:
            newG[neighbour].remove(u)
        newG[u] = set()

        return VertexCover2(newG, E, k - 1, newC)         
    elif maxDegree > 2:

        newC = C.copy()
        newC.add(u)

        newG = G.copy()
        neighbours = G[u].copy()

        for neighbour in G[u]:
            newG[neighbour].remove(u)
        newG[u] = set()        

        S1 = VertexCover(newG, E, k - 1, newC)
        return S1

    return set()
#

def main(name):
    G = loadGraph( name )
    E = edgeList(G)

    for k in range(1, len(G) + 1):
        C = VertexCover2(G, E, k, set())
        if len(C) > 0: 
            saveSolution(name + '.sol', C)
            return
        
    saveSolution(name + '.sol', [-1])
# end main2() procedure 

from multiprocessing import Process
from removeOld import removeOldSolutions

# 28/29 VertexCover

if __name__ == '__main__':
    removeOldSolutions()
    counter = 0
    n = len(graphs)

    for nameGraph in graphs:
        counter += 1
        name = f"graph/{nameGraph}"
        print(f"{counter}/{n} {name}")
        
        p = Process(target=main, args=(name,))
        p.start()
        p.join(timeout=5)
        if p.is_alive():
            p.terminate()
            p.join()
            saveSolution(name + '.sol', [0])
            print("\033[93mTime limit exceeded\033[0m")
    #
#