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

def remove_edges(E, vertices):
    return [(x, y) for (x, y) in E if x not in vertices and y not in vertices]

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

    newCU = C.copy()
    newC = C.copy()
    newCU.add(u)

    for vertex in G[u]:
        newC.add(vertex)

    E1 = remove_edges(E, {u})
    S1 = VertexCover(G, E1, k - 1, newCU)

    E2 = remove_edges(E, G[u])
    S2 = VertexCover(G, E2, k - len(G[u]), newC)

    if S1:
        return S1 
    if S2:
        return S2 
    
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




