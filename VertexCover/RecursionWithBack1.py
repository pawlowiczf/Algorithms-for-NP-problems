from itertools import *
from dimacs import *

# 'Usuwamy' wierzchołki grafu - czyli wybieramy rekurencyjnie dany wierzchołek do pokrycia. 

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
    #
    if k == 0: 
        return set() 
    
    for (u, v) in E:
        if (u not in C) and (v not in C):
            break 
    else:
        return C
    
    newE = [e for e in E if e != (u, v)]

    C.add(u)
    S1 = VertexCover(G, newE, k - 1, C)
    if S1:
        return S1 
    C.remove(u)

    C.add(v)   
    S2 = VertexCover(G, newE, k - 1, C)
    if S2:
        return S2 
    C.remove(v)    

    return set()
# end VertexCover() procedure 

def main(name):
    G = loadGraph( name )
    E = edgeList(G)

    for k in range(1, len(G) + 1):
        C = VertexCover(G, E, k, set())
        if len(C) > 0: 
            saveSolution(name + '.sol', C)
            break
    #
# end main() procedure 

# 14/29 VertexCover

from multiprocessing import Process
from removeOld import removeOldSolutions

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



