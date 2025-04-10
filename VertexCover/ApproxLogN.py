from copy import deepcopy
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
("k330_d"),
("k330_e"),
("k330_f"),
("f30"),
("f35"),
("f40"),
("f56"),
("m20"),
("m30"),
("m40"),
("m50"),
("m100"),
("p20"),
("p35"),
("p60"),
("p150"),
("p200"),
("r30_01"),
("r30_05"),
("r50_001"),
("r50_01"),
("r50_05"),
("r100_005"),
("r100_01"),
("r200_001"),
("r200_005")
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

def VertexCover(G):
    C = set()

    while not hasNoEdges(G):
        u = 0
        for vertex, N_vertex in enumerate(G):
            if len(N_vertex) > len(G[u]): u = vertex 
        #
        C.add(u)

        G = without(G, {u})
    #
    
    return C 
#

def main(name):
    G = loadGraph( name )

    C = VertexCover(G)
    if len(C) > 0: 
        saveSolution(name + '.sol', C)
        return
        
    saveSolution(name + '.sol', [0])
# end main() procedure 

from multiprocessing import Process
from removeOld import removeOldSolutions

# /29 VertexCover

if __name__ == '__main__':
    removeOldSolutions()
    counter = 0
    n = len(graphs)

    for nameGraph in graphs:
        counter += 1
        name = f"graph2/{nameGraph}"
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