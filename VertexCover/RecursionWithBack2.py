from itertools import *
from dimacs import *

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

def removeEdges(E, vertex):
    return [(x, y) for (x, y) in E if x != vertex and y != vertex]

def VertexCover(G, E, k, C):
    #
    if k < 0: return set() 
    if len(E) == 0: return C 
    if k == 0: return set() 

    
    u = -1
    for vertex in range(len(G)):
        if vertex not in C and len(G[vertex]) > 0:
            u = vertex 
            break 
    
    if u == -1: return set()

    newE = removeEdges(E, u)

    C.add(u)
    S1 = VertexCover(G, newE, k - 1, C)
    if S1:
        return S1 
    C.discard(u)

    for vertex in G[u]:
        C.add(vertex)
    S2 = VertexCover(G, newE, k - len(G[u]), C)
    if S2:
        return S2 
    for vertex in G[u]:
        C.discard(vertex)

    return set()
# end VertexCover() procedure 

def main():
    counter = 0 

    for name in graphs:
        flag = False 
        counter += 1 
        print(f"{counter}/{len(graphs)}: {name} ")

        name = f"graph/{name}"
        G = loadGraph( name )
        E = edgeList(G)

        for k in range(1, len(G) + 1):
            C = VertexCover(G, E, k, set())
            if len(C) > 0: 
                saveSolution(name + '.sol', C)
                flag = True 
                break

        if not flag:
            saveSolution(name + '.sol', [0])
    #

# end main() procedure 

main() 




