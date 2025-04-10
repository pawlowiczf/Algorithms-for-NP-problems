import os 
import pycosat     
from dimacs import loadX3CWithSolution

path = "./graphs-x3c/"
files = [entry.name for entry in os.scandir(path) if entry.is_file()]

def ReductionX3CToSAT(sets, n):
    belongsTo = {} # dict: element -> [sets which it belongs to]

    for idx in range(len(sets)):
        for element in sets[idx]:
            if element not in belongsTo: 
                belongsTo[element] = [idx + 1]
            else:
                belongsTo[element].append(idx + 1)
    # end 'for' loops 

    formula = [] 
    
    for _, (element, occurrences) in enumerate(belongsTo.items()):
        formula.append(occurrences)

        if len(occurrences) == 1: continue 
        if len(occurrences) == 2:
            formula.append([-occurrences[0], -occurrences[1]])
            continue
        if len(occurrences) == 3:
            formula.append([-occurrences[0], -occurrences[1]])
            formula.append([-occurrences[0], -occurrences[2]])
            formula.append([-occurrences[1], -occurrences[2]])
            continue
    #
    
    return formula 
#

def main():
    counter, numberOfTests = 1, len(files)
    goodSolutionCounter = 0

    for name in files:
        n, sets, isPossible = loadX3CWithSolution(f'{path}{name}')
        formula = ReductionX3CToSAT(sets, n)

        result = pycosat.solve(formula)
        if result == 'UNSAT': result = False 
        else: result = True 

        if result == isPossible: goodSolutionCounter += 1
        print(f"{counter}/{numberOfTests}: {name} - {result == isPossible}")
        counter += 1
    #

    print(f'{goodSolutionCounter}/{numberOfTests}')
# end procedure main()

main()