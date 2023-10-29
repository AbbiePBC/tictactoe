"""
Tic Tac Toe Player
"""

import math
import copy

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

def player(board) -> int:
    """
    Returns player who has the next turn on a board.
    """

    num_x = sum(sum(1) for x in board if x == X)
    num_o = sum(sum(1) for o in board if o == O)

    return X if num_x > num_o else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves: set(tuple[int, int]) = set()
    for row_idx in range(3):
        for box_idx in range(3):
            if board[row_idx][box_idx] == EMPTY:
                possible_moves.add((row_idx, box_idx))

    return possible_moves


def result(board, action) -> tuple[list[list[str]], str]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player

    return (new_board, current_player)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]
    
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) or len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if not w:
        return 0
    if w == X:
        return 1
    if w == O:
        return -1


def X_action(board) -> tuple[int, int]:
    """
    Optimise for max value of X
    """
    value = 10000
    action_to_take = tuple[int, int]
    if terminal(board):
        return utility(board)
    for action in actions(board):
        min_possible_result_from_action = result(board, action)
        if value < min_possible_result_from_action:
            value = min_possible_result_from_action
            action_to_take = action
    return value, action_to_take

def O_action(board) -> tuple[int, tuple[int, int]]:
    """
    Optimise for min value of O
    """
    value = -10000
    action_to_take = tuple[int, int]
    if terminal(board):
        return utility(board)
    for action in actions(board):
        max_possible_result_from_action = result(board, action)
        if value > max_possible_result_from_action:
            value = max_possible_result_from_action
            action_to_take = action
    return value, action_to_take

def minimax(board) -> tuple[int, tuple[int, int]]:
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if current_player == X:
        return X_action
    elif current_player == O:
        return O_action
    else:
        raise ValueError

    
