from itertools import permutations 
from collections import Counter
import random

vs = [-1,0,1]

simple = [(-1,-1), (0,-1), (1,-1),
          (-1,0), (0,0), (1,0),
          (-1,1), (0,1), (1,1)]

def init():
    return {(x,y): ' ' for x in vs for y in vs}

def count(board, sym):
    return len([s for s in board.values() if s == sym])

def countl(line, sym):
    return len([s for s, p in line if s == sym])

def lines(board):
    lines = []
    for x in vs:
        lines.append([(board[(x, y)], (x,y)) for y in vs])
    for y in vs:
        lines.append([(board[(x, y)], (x,y)) for x in vs])
    lines.append([(board[(x, x)], (x,x)) for x in vs])
    lines.append([(board[(x, y)], (x,y)) for x, y in [(-1, 1), (0, 0), (1, -1)]])
    return lines

def valid(board):
    cx = count(board, 'X')
    co = count(board, 'O')
    return cx == co + 1 or cx == co

def move(board, rule):
    cx = count(board, 'X')
    co = count(board, 'O')
    if cx == co + 1:
        return move1(board, rule, 'O'), 'O'
    elif cx == co:
        return move1(board, rule, 'X'), 'X'
    else:
        assert False

def other(sym):
    return 'O' if sym == 'X' else 'X'

def next_win(line, sym):
    return countl(line, sym) == 2 and countl(line, ' ') == 1

def win(line, sym):
    return countl(line, sym) == 3

def winner(board):
    for sym in ['X', 'O']:
        if any(win(line, sym) for line in lines(board)):
            return sym
    if count(board, ' ') == 0:
        return None
    else:
        return False

def empty(line):
    for s,p in line:
        if s == ' ':
            return p
    assert False

def move1(board, rule, sym):
    ms = moves(board, rule, sym)
    return ms[0]

def play(board, ais):
    pc = 0
    while winner(board) is False:
        m, sym = move(board, ais[pc])
        board[m] = sym
        pc = 1 - pc
        assert valid(board), board
    return winner(board)

# return a list of valid moves from a position
def moves(board, rule, sym):
    ms = []
    ls = lines(board)
    for line in ls:
        if next_win(line, sym):
            ms.append(empty(line))
            return ms

    for line in ls:
        if next_win(line, other(sym)):
            ms.append(empty(line))
            return ms

    for p in rule:
        if board[p] == ' ':
            ms.append(p)
    return ms

def show(board):
    for y in vs:
        for x in vs:
            print(board[(x,y)] + '|', end='')
        if y == 1:
            print('\n======')
        else:
            print('\n------')

def rand(wins):
    random.shuffle(simple)
    ai1 = simple
    random.shuffle(simple)
    ai2 = simple
    b = init()
    print(ai1, ai2)
    res = play(b, [ai1, ai2])
    if res == 'X':
        wins[tuple(ai1)] += 1
    elif res == 'O':
        wins[tuple(ai2)] += 1
    show(b)
    print(res)
    
def repeat():
    wins = Counter()
    for _ in range(10000):
        rand(wins)
    for ai in wins:
        print(ai, wins[ai])

def test():
    b = init() | {(-1,0): 'X', (1,0): 'X'}
    move1(b, simple, 'O')
    show(b)
    b = init()
    play(b, [simple, simple])
    show(b)
    print(winner(b))

def testsim():
    cnt = {'X':0, 'O':0, None:0}
    sim(init(), simple, cnt)
    print(cnt)
            
if __name__ == "__main__":
    repeat()
