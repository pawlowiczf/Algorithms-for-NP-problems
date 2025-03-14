import sys 

def canMoveTo(B, W, H, y, x):
    return B[y][x] != '#' and B[y][x] != 'O'
#

moves = {
    "G": (-1, 0),
    "D": (1, 0),
    "P": (0, 1),
    "L": (0, -1)
}

# B - board, W - width, H - height, S - number of snacks
def BruteForce(B, W, H, S, y, x, alreadyEaten, path):
    if alreadyEaten == S: return True 
    alreadyEatenCopy = alreadyEaten
    
    for move, (dfY, dfX) in moves.items():
        restorer = []
        newY, newX = y + dfY, x + dfX 

        while canMoveTo(B, W, H, newY, newX):

            restorer.append((newY, newX, B[newY][newX]))
            if B[newY][newX] == '*': alreadyEaten += 1
            B[newY][newX] = '#'   

            newY, newX = newY + dfY, newX + dfX 
        # end 'while' loop
        
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

