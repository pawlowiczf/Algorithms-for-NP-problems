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

def VertexCover(G, E, k, C):
    u, v = -1, -1
    for (x, y) in E:
        if (x not in C) and (y not in C):
            u, v = x, y
            break 
    #


    if u == -1 and v == -1: 
        return C 
    newE = E.copy()
    newE.remove((u, v))
    
    if k == 0: 
        return set() 

    newCU = C.copy()
    newCV = C.copy()
    newCU.add(u)
    newCV.add(v)

    S1 = VertexCover(G, newE, k - 1, newCU)
    S2 = VertexCover(G, newE, k - 1, newCV)

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




