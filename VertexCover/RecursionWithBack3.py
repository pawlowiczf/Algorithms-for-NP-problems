from itertools import *
from dimacs import *
from copy import deepcopy

graphs = [
("e5"),
("e10"),
("e20"),
("e40"),
("e150"),
("s25"),
("s50"),
("s500"),
("b20"),
("b30"),
("b100"),
("k330_a"),
("k330_b"),
("k330_c"),
("m20"),
("m30"),
("m40"),
("m50"),
("m100"),
("p20"),
("p35"),
("p60"),
("p150"),
("r30_01"),
("r30_05"),
("r50_001"),
("r50_01"),
("r50_05"),
("r100_005"),
]

def hasNoEdges(G):
    return not any(G)
#

def without(G, vertices):
    G = deepcopy(G)
    for vertex in vertices:
        for neighbour in G[vertex]:
            G[neighbour].remove(vertex)
        #
        G[vertex].clear()
    #

    return G
#

def VertexCover(G, k, C):
    #
    if k < 0: return set()
    if hasNoEdges(G): return C
    if k == 0: return set() 

    u = 0
    
    # Find a vertex 'u' with degree == 1
    for vertex, N_vertex in enumerate(G):
        if len(N_vertex) == 1: 
            return VertexCover(without(G, {vertex} | N_vertex), k - 1, C | N_vertex) 
        #
        if len(N_vertex) > len(G[u]): u = vertex 
    #

    S = VertexCover(without(G, {u}), k - 1, C | {u})         
    if S: return S

    N_u = G[u]
    S = VertexCover(without(G, N_u), k - len(N_u), C | N_u)
    if S: return S

    return set()
#

def main(name):
    G = loadGraph( name )

    for k in range(1, len(G) + 1):
        C = VertexCover(G, k, set())
        if len(C) > 0: 
            saveSolution(name + '.sol', C)
            return
        
    saveSolution(name + '.sol', [-1])
# end main2() procedure 

from multiprocessing import Process
from removeOld import removeOldSolutions

# 23/29 VertexCover

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