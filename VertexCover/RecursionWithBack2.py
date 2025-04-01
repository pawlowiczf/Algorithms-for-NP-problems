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

# def removeEdges(E, vertices):
#     return [(x, y) for (x, y) in E if x not in vertices and y not in vertices]
# #

# def VertexCover(G, E, k, C):
#     #
#     if k < 0: return set() 
#     if len(E) == 0: return C 
#     if k == 0: return set() 

#     # Find a vertex 'u' with degree > 0.
#     u, _ = E[0]

#     newG = G.copy()
#     newE = removeEdges(E, {u})
#     newC = C.copy()
#     newG[u] = set()
#     newC.add(u)
#     S1 = VertexCover(newG, newE, k - 1, newC)
#     if S1: return S1 

#     newG = G.copy() 
#     newC = C.copy()
#     vertices = set()
#     for neighbour in G[u]:
#         vertices.add(neighbour)
#         newG[neighbour] = set()
#     newE = removeEdges(E, vertices)
#     S2 = VertexCover(newG, newE, k - len(vertices), newC.union(vertices))
#     if S2: return S2 

#     return set()
# #

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

def VertexCover2(G, k, C):
    if k < 0: return set() 
    if hasNoEdges(G): return C
    if k == 0: return set()

    for u, N_u in enumerate(G):
        if N_u: break 
    #

    S1 = VertexCover2(without(G, {u}), k - 1, C | {u})
    if S1: return S1 

    S2 = VertexCover2(without(G, N_u), k - len(N_u), C | N_u)
    if S2: return S2 

    return set()
#

# def main(name):
#     G = loadGraph( name )
#     E = edgeList(G)

#     for k in range(1, len(G) + 1):
#         C = VertexCover(G, E, k, set())
#         if len(C) > 0: 
#             saveSolution(name + '.sol', C)
#             return
        
#     saveSolution(name + '.sol', [-1])
# end main() procedure 

def main2(name):
    G = loadGraph( name )
    E = edgeList(G)

    for k in range(1, len(G) + 1):
        C = VertexCover2(G, k, set())
        if len(C) > 0: 
            saveSolution(name + '.sol', C)
            return
        
    saveSolution(name + '.sol', [-1])
# end main2() procedure 

from multiprocessing import Process
from removeOld import removeOldSolutions

# 15/29 VertexCover

if __name__ == '__main__':
    removeOldSolutions()
    counter = 0
    n = len(graphs)

    for nameGraph in graphs:
        counter += 1
        name = f"graph/{nameGraph}"
        print(f"{counter}/{n} {name}")
        
        p = Process(target=main2, args=(name,))
        p.start()
        p.join(timeout=5)
        if p.is_alive():
            p.terminate()
            p.join()
            saveSolution(name + '.sol', [0])
            print("\033[93mTime limit exceeded\033[0m")
    #
#




