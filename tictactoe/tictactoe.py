"""
Tic Tac Toe Player
"""
from sys import _xoptions
import math
import copy
from queue import Empty
from urllib.parse import non_hierarchical



X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    Xs = 0
    Os = 0
    for A in board:
        for B in A:
            if 'X' == B:
                Xs = Xs + 1
            if 'O' == B:
                Os = Os + 1

    if Xs == Os:
        return 'X'
    elif Xs > Os:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range (3):
        for j in range (3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] != EMPTY:
        return Exception
    else:
        new_board[action[0]][action[1]] = player(board)

    return new_board 



def winner(board):

    first = 0
    second = 0
    third = 0
    firstc = 0
    secondc = 0
    thirdc = 0
    for index, row in enumerate(board):
        if row[0] != None and row[0] == row[1] and row[0] == row[2]:
            return row[0]
        if index == 0 and row[0] != None:
            first = row[0]
            firstc = 1
        if index == 1 and row[0] == first:
            firstc += 1
        if index == 2 and row[0] == first:
            if firstc == 2:
                return first
        if index == 0 and row[1] != None:
            second = row[1]
            secondc += 1
        if index == 1 and row[1] == second:
            secondc += 1
        if index == 2 and row[1] == second:
            if secondc == 2:
                return second
        if index == 0 and row[2] != None:
            third = row[2]
            thirdc = 1
        if index == 1 and row[2] == third:
            thirdc += 1
        if index == 2 and row[2] == third:
            if thirdc == 2:
                return third
    A = 0
    B = 0 
    countA = 0
    countB = 0
    for index, row in enumerate(board):
        if index == 0 and row[0] != None:
            A = row[0]
            countA = 1
        if index == 1 and row[1] == A:
            countA += 1
        if index == 2 and row[2] == A:
            countA += 1
            if countA == 3:
                return A
        if index == 0 and row[2] != None:
            B = row[2]
            countB = 1
        if index == 1 and row[1] == B:
            countB += 1
        if index == 2 and row[0] == B:
            countB += 1
            if countB == 3:
                return B
    
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        if row[0] == EMPTY or row[1] == EMPTY or row[2] == EMPTY:
            return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    temp = winner(board)
    if temp == X:
        return 1
    if temp == O:
        return -1
    if temp == None:
        return 0

def minimax(board):

    if terminal(board):
        return None
    pl = player(board)
    acts = actions(board)
    if pl == X:
        v = float('-inf')
        for action in acts:
            rslt = result(board, action)
            if terminal(rslt):
                if utility(rslt) > v:
                    v = utility(rslt)
                    optimal = action 
            else:
                ut = Min(rslt)
                if ut > v:
                    v = ut
                    optimal = action
        return optimal
    elif pl == O:
        v = float('inf')
        for action in acts:
            rslt = result(board, action)
            if terminal(rslt):
                if utility(rslt) < v:
                    v = utility(rslt)
                    optimal = action
            else:
                ut = Max(rslt)
                if ut < v:
                    v = ut
                    optimal = action
        return optimal
 
def Min(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    acts = actions(board)
    for action in acts:
        rslt = result(board, action)
        if terminal(rslt):
            if utility(rslt) < v:
                v = utility(rslt)
                if v == -1:
                    return v
        else:
            ut = Max(rslt)
            if ut < v:
                v = ut
                if v == -1:
                    return v
    return v

def Max(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    acts = actions(board)
    for action in acts:
        rslt = result(board, action)
        if terminal(rslt):
            if utility(rslt) > v:
                v = utility(rslt)
                if v == 1:
                    return v
        else:
            ut = Min(rslt)
            if ut > v:
                v = ut
                if v == 1:
                    return v


    return v

 



