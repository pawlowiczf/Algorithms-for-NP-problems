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

def singleVariableClause(CNF):
    if CNF is None: return None 

    for clause in CNF:
        if len(clause) == 1: return clause 
    return None 
#

from copy import deepcopy

def unitPropagate( CNF, V ):
    #
    newCNF = simplifyCNF(CNF, V)
    if newCNF is None: return None 

    while (clause := singleVariableClause(newCNF)) != None:
        variable = clause[0]
        v = abs(variable)
        requiredValue = 1 if variable > 0 else -1 

        if v in V:
            if V[v] != requiredValue: return None 
            else:
                newCNF = simplifyCNF(CNF, V)
                if newCNF is None: return None 
                continue 
        #
        #  
        if variable < 0: V[v] = -1 
        else: V[v] = 1 

        newCNF = simplifyCNF(newCNF, V)
        if newCNF is None: return None
    #

    return newCNF
# end procedure

def findPureVariables(CNF):
    pure = {} 
    for clause in CNF:
        for variable in clause:
            v = abs(variable)
            sign = 1 if variable > 0 else -1 

            if v not in pure:
                pure[v] = sign 
            elif pure[v] != sign:
                pure[v] = 0 
    #

    pure = [(v, sign) for v, sign in pure.items() if sign != 0]
    return pure if len(pure) > 0 else None 
# end procedure 

def removePureVariables(CNF, V):
    newCNF = deepcopy(CNF)

    while (pures := findPureVariables(newCNF)) is not None: 
        for v, sign in pures: 
            if v in V:
                if V[v] != sign: return None 
            else:
                V[v] = sign 
        #
        newCNF = simplifyCNF(newCNF, V)
        if newCNF is None: return None 
    #

    return newCNF
# end procedure 

def simplifyFormula(CNF, V):
    while True:
        cnf_after_unit = unitPropagate(CNF, V)
        if cnf_after_unit is None:
            return None
        
        cnf_after_pure = removePureVariables(cnf_after_unit, V)
        if cnf_after_pure is None:
            return None
        
        if cnf_after_pure == CNF:
            break
        CNF = cnf_after_pure
    
    return CNF
# end procedure 

def SolverSAT( CNF, oldV ):
    # CNF to rozważana formuła
    # V to wartościowanie zmiennych
    V = oldV.copy()

    simplifiedCNF = simplifyFormula(CNF, V)
    if simplifiedCNF is None: return "UNSAT"
    if len(simplifiedCNF) == 0: return V # formula is satisfied, no clauses left 

    # simplifiedCNF = unitPropagate(CNF, V)
    # if simplifiedCNF is None: return "UNSAT"
    # if len(simplifiedCNF) == 0: return V # formula is satisfied, no clauses left 

    # simplifiedCNF = removePureVariables(simplifiedCNF, V)
    # if simplifiedCNF is None: return "UNSAT"
    # if len(simplifiedCNF) == 0: return V # formula is satisfied, no clauses left 

    clause = simplifiedCNF[0]

    for variable in clause:
        v = abs(variable) 
        if v in V: continue

        if variable < 0: V[v] = -1 
        else: V[v] = 1 

        result = SolverSAT( CNF, V )
        if result != "UNSAT": return result    

        if variable < 0: V[v] = 1 
        else: V[v] = -1
    #
    for variable in clause:
        v = abs(variable)
        if v in V:
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

main(bigSATs)