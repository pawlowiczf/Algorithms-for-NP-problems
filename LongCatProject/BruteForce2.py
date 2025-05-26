import sys 
from collections import deque

def canMoveTo(B, W, H, y, x):
    return B[y][x] != '#' and B[y][x] != 'O'
#

moves = {
    "D": (1, 0),
    "G": (-1, 0),
    "P": (0, 1),
    "L": (0, -1)
}

def getValidNeighbours(B, W, H, y, x):
    neighbours = [] 
    for move, (dfY, dfX) in moves.items():
        nY, nX = y + dfY, x + dfX 
        if canMoveTo(B, W, H, nY, nX):
            neighbours.append((nY, nX))
    #
    return neighbours
#

# startY, startX - last valid position 
def canContinueSearch(B, W, H):

    visited = [ [False for _ in range(W)] for _ in range(H) ]

    def BFS(y, x):
        queue = deque()
        queue.append((y, x))
        visited[y][x] = True 

        while queue:
            sY, sX = queue.popleft()
            for (nY, nX) in getValidNeighbours(B, W, H, sY, sX):
                if not visited[nY][nX]:
                    visited[nY][nX] = True 
                    queue.append((nY, nX))
            #
        #
    # end procedure BFS()

    lakesFound = 0 
    for y in range(H):
        for x in range(W):
            if visited[y][x] == False and B[y][x] == '*':
                BFS(y, x)
                lakesFound += 1
                if lakesFound >= 2: return False 
    #

    return True 
#

# B - board, W - width, H - height, S - number of snacks
def BruteForce(B, W, H, S, y, x, alreadyEaten, path):
    if alreadyEaten == S: return True 
    alreadyEatenCopy = alreadyEaten
    
    # Sprawdz wszystkie możliwe ruchy w danym miejscu (gora, dol, prawo , lewo)
    for move, (dfY, dfX) in moves.items():
        restorer = []
        newY, newX = y + dfY, x + dfX 

        # Skoro wybrałeś by poruszać się np. w górę, to musisz iść tam cały czas, 
        # dopóki nie natrafisz na prezszkodę
        while canMoveTo(B, W, H, newY, newX):

            restorer.append((newY, newX, B[newY][newX]))
            if B[newY][newX] == '*': alreadyEaten += 1
            B[newY][newX] = '#'   

            newY, newX = newY + dfY, newX + dfX 
        # end 'while' loop
        
        if y % 2 == 0 and x % 2 == 0:
            if not canContinueSearch(B, W, H):
                for (oldY, oldX, oldValue) in restorer:
                    B[oldY][oldX] = oldValue
                alreadyEaten = alreadyEatenCopy
                continue 
        
        # dodaj ruch do wyniku, przesuń się na odpowiednie pole i sprawdź rekurencyjnie, czy 
        # taki ruch zapewnia wygraną. Jeśli nie, to usuń ten ruch z wyniku oraz usuń całą trasę (restorer). 
        path.append(move)
        if len(restorer) > 0: 
            newY, newX = restorer[-1][0], restorer[-1][1]
            if BruteForce(B, W, H, S, newY, newX, alreadyEaten, path): return path 
        path.pop()

        for (oldY, oldX, oldValue) in restorer:
            B[oldY][oldX] = oldValue
        #
        
        alreadyEaten = alreadyEatenCopy
    # end 'for' loop     

    return False 
# end procedure BruteForce()

def main():
    firstLine = sys.stdin.readline().strip()
    W, H, S = firstLine.split(sep=' ')
    W, H, S = int(W), int(H), int(S)
    
    # Czytanie ze standardowego wejścia
    B = [[None for _ in range(W)] for _ in range(H)]
    y, x = -1, -1 
    counter = 0
    for line in sys.stdin:
        line = line.strip()
        for idx in range(W):
            if line[idx] == 'O':
                y, x = counter, idx 
            B[counter][idx] = line[idx]
        #
        counter += 1
#

    result = BruteForce(B, W, H, S, y, x, 0, [])
    print(''.join(result))
# end procedure main()

main()

