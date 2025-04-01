#!/usr/bin/python3

from copy import deepcopy
import sys

RERAISE = False


def getboard( board, cat ):
  x = cat[0]
  y = cat[1]
  try:
    return board[y][x]
  except Exception as e:
    return "#"


def putboard( board, cat, sym ):
  x = cat[0]
  y = cat[1]
  try:
    board[y][x] = sym
  except Exception as e:
    pass
  



def readBoard( fname ):
  f=open(fname)
  W,H,S = f.readline().strip('\n').split()
  W = int(W)
  H = int(H)
  S = int(S)
  board = []
  for i in range(H):
    line = f.readline().strip()
    line = [ d for d in line ]
    if len( line ) != W: raise Exception("Zla dlugosc wiersza w opisie planszy")
    board += [line]

  cat = [-1,-1]
  found_cat = 0
  for y in range(H):
    for x in range(W):
      if getboard( board, [x,y] ) == "O":
        cat = [x,y]
        found_cat += 1

  if found_cat != 1:
    raise Exception("Legowisko musi byc dokladnie jedno")
        
  return W,H,S, board, cat
    
    
def readSolution( fname ):
  sol = ""
  f = open(fname)
  try:
    sol = f.readline().strip('\n')
  except Exception as e:
    raise Exception(f"Problem z odczytaniem rozwiazania")  
                 
  return sol




def drawBoard( board, S ):
  for line in board:
    print( "".join(line))
  print(f"Pozostale smaczki do zjedzenia: {S}")
  print()


DIR = {"G": (0,-1),
       "D": (0,1), 
       "L": (-1,0), 
       "P": (1,0)
      }


BLOCK = {"#":"#",
         "O":"#",
         "X":"#",
         ".":".",
         "*":"."}




def makeMove( board, cat, dir ):
  ate = 0 
  while True:
    try: 
      cat[0] += DIR[dir][0]
      cat[1] += DIR[dir][1]
    except Exception as e:
      raise Exception(f"Bledny kierunek ruchu kota? (kierunek = '{dir}')")
    block = getboard( board, cat )
    if BLOCK[block] == ".":
      if block == "*": ate += 1
      putboard( board, cat, "X" )
    else:
      cat[0] -= DIR[dir][0]
      cat[1] -= DIR[dir][1]
      return ate



    




if __name__=="__main__":
  if len(sys.argv)<3:
    print("Wywołanie:\n   judge.py <infile> <outfile> [-v]")
  else:
    view = len(sys.argv)==4 and sys.argv[3]=='-v'

    try:
      W,H,S,board, cat = readBoard(sys.argv[1])
      sol = readSolution(sys.argv[2] )
      if view: drawBoard( board, S )

      for dir in sol:
        S -= makeMove( board, cat, dir )
        if view:
          drawBoard( board, S )
        
    

      if S <= 0:
        print('OK')
        exit(0)
      else:
        raise Exception("Glodny kot jest glodny")
        exit(1)
    except Exception as e:
      print("WRONG")
      print(e)
      if RERAISE: raise e
      exit(1)
