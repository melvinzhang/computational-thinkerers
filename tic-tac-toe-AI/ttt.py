import itertools
from collections import Counter
import random
import pickle
import os
import sys

vs = [-1,0,1]

simple = ((-1,-1), (0,-1), (1,-1),
          (-1, 0), (0, 0), (1, 0),
          (-1, 1), (0, 1), (1, 1))

def init():
    return {(x,y): ' ' for x in vs for y in vs}

def count(board, sym):
    return sum(1 for s in board.values() if s == sym)

def countl(line, sym):
    return sum(1 for s, p in line if s == sym)

def lines(board):
    lines = []
    for x in vs:
        lines.append([(board[(x, y)], (x, y)) for y in vs])
    for y in vs:
        lines.append([(board[(x, y)], (x, y)) for x in vs])
    lines.append([(board[(x, y)], (x, y)) for x, y in zip(vs, vs)])
    lines.append([(board[(x, y)], (x, y)) for x, y in zip(vs, reversed(vs))])
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

def comp(p, q):
    board = init()
    w = play(board, [p, q])
    if w == 'X':
        return -1
    elif w == 'O':
        return 1
    else:
        return 0

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

def rand_ai(won, lost):
    if len(lost) > len(won) * 500:
        return random.choice(tuple(won))
    p = tuple(random.sample(simple, k=len(simple)))
    while p in lost:
        p = tuple(random.sample(simple, k=len(simple)))
    return p

def restore():
    if not os.path.exists('progress.pkl'):
        return set(), set()
    with open('progress.pkl', 'rb') as f:
        rec = pickle.load(f)
        lost = rec['lost']
        won = rec['won']
    return won, lost

def save(won, lost):
    with open('temp.pkl', 'wb') as f:
        pickle.dump({'won': won, 'lost': lost}, f)
    os.replace('temp.pkl', 'progress.pkl')

def outcome(w, l, won, lost):
    won.add(w)
    won.discard(l)
    lost.add(l)

# single elimination until less than 30 left
# save progress after every 1000 matches
def tournament():
    won, lost = restore()
    for i in itertools.count():
        if i % 1000 == 0:
            print(len(won), len(lost), len(won)+len(lost))
            save(won, lost)
        p = rand_ai(won, lost)
        q = rand_ai(won, lost)
        r = comp(p, q) - comp(q, p)
        if r <= -1:
            outcome(p, q, won, lost)
        elif r >= 1:
            outcome(q, p, won, lost)
        if len(lost) > 200000 and len(won) < 30:
            save(won, lost)
            break
    
def test():
    b = init() | {(-1,0): 'X', (1,0): 'X'}
    assert move1(b, simple, 'O') == (0, 0)
    b = init()
    play(b, [simple, simple])
    assert b == {(-1, -1): 'X', (-1, 0): 'O', (-1, 1): 'X', (0, -1): 'O', (0, 0): 'X', (0, 1): ' ', (1, -1): 'X', (1, 0): ' ', (1, 1): 'O'}
    assert winner(b) == 'X'
    assert stats(simple) == {'first': {'win': 6, 'lose': 7, 'draw': 23}, 'second': {'win': 31, 'lose': 67, 'draw': 151}}
    assert stats((perm2pos([6, 3, 7, 2, 8, 4, 9, 5, 1]))) == {'first': {'win': 62, 'lose': 1, 'draw': 66}, 'second': {'win': 30, 'lose': 48, 'draw': 307}}

def sim(ai, ai_sym):
    cnt = {'win':0, 'lose':0, 'draw':0}
    sim_r(init(), ai, ai_sym, 'X', cnt)
    return cnt

def win2res(w, sym):
    if w is None:
        return 'draw'
    elif w == sym:
        return 'win'
    elif w == other(sym):
        return 'lose'
    else:
        assert False

def sim_r(board, ai, ai_sym, sym, cnt):
    ms = moves(board, ai, sym)
    if sym == ai_sym:
        ms = [ms[0]]
    for m in ms:
        board[m] = sym
        w = winner(board)
        if w is False:
            sim_r(board, ai, ai_sym, other(sym), cnt)
        else:
            cnt[win2res(w, ai_sym)] += 1
        board[m] = ' '

def stats(ai):
    return {'first': sim(ai, 'X'), 'second': sim(ai, 'O')}

def pos2perm(rules):
    perm = [None] * 9
    for i, p in enumerate(rules):
        j = simple.index(p)
        perm[j] = i+1
    return perm

def perm2pos(perm):
    pos = [None] * 9
    for i, p in enumerate(perm):
        pos[p - 1] = simple[i]
    return pos

def winners():
    seen = set()
    won, _ = restore()
    for p in won:
        st = stats(p)
        rep = repr(st)
        if rep not in seen:
            seen.add(rep)
            print(pos2perm(p), st)

if __name__ == "__main__":
    name = sys.argv[1]
    locals()[name]()
