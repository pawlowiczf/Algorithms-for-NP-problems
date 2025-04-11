from satLists import *
from dimacs import loadCNF

def simplifyClause( C, V ):
    # C - klauzula, czyli lista literałów
    # V - wartościowanie zmiennych

    newC = []

    for variable in C:
        if abs(variable) in V:
            value = V[abs(variable)]
            if variable > 0 and value == 1: return None # clause is satisfied  
            if variable < 0 and value == -1: return None # clause is satisfied  
        else:
            newC.append(variable)
    #

    return newC 
# end procedure 

def simplifyCNF( CNF, V ):
    # CNF - formuła do uproszczenia
    # V   - wartościowanie zmiennych

    newFormula = []

    for clause in CNF:
        simplifiedClause = simplifyClause(clause, V)
        if simplifiedClause is None: continue # clause is satisfied, we can skip it
        if len(simplifiedClause) == 0: return None # clause is never satisfied, formula either 

        newFormula.append(simplifiedClause)
    #

    return newFormula 
# end procedure 

path = './sats/'

def SolverSAT( CNF, V ):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych

    simplifiedCNF = simplifyCNF(CNF, V)
    if simplifiedCNF is None: return "UNSAT"
    if len(simplifiedCNF) == 0: return V # formula is satisfied, no clauses left 

    v = abs(simplifiedCNF[0][0])

    V[v] = 1 
    result = SolverSAT( simplifiedCNF, V )
    if result != "UNSAT": return result 
    del V[v]

    V[v] = -1
    result = SolverSAT( simplifiedCNF, V )
    if result != "UNSAT": return result 
    del V[v]

    return "UNSAT"
# end procedure 

def main(files):
    counter, numberOfTests = 1, len(files)
    goodSolutionCounter = 0

    for name in files:
        n, CNF, isPossible = loadCNF(f'{path}{name}')
        V = {}
        result = SolverSAT(CNF, V)

        if result == "UNSAT": result = False 
        else: result = True 

        result = isPossible == result 
        if result: goodSolutionCounter += 1
        print(f"{counter}/{numberOfTests}: {name} - {result}")
        counter += 1
    #

    print(f'{goodSolutionCounter}/{numberOfTests}')
# end procedure main()

main(smallSATs)