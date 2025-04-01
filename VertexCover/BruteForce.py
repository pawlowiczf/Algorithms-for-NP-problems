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

def VertexCover(G, E, k):
    #
    for C in combinations( range(len(G)), k ):
        if isVC(E, C):
            return C
    #

    return []
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
            C = VertexCover(G, E, k)
            if len(C) > 0: 
                saveSolution(name + '.sol', C)
                flag = True 
                break

        if not flag:
            saveSolution(name + '.sol', [])
    #

# end main() procedure 

main() 




