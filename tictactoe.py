"""
Tic Tac Toe Player
"""

import logging
import copy
from typing import Optional

X = "X"
O = "O"
EMPTY = None
Action = tuple[int, int]
logging.basicConfig(level=logging.INFO)

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board) -> str:
    """
    Returns player who has the next turn on a board.
    """

    num_x, num_o = 0, 0
    for row in board:
        for i in row:
            if i == X:
                num_x += 1
            if i == O:
                num_o += 1
    logging.info(f"Current player: {X if num_x <= num_o else O}")
    return X if num_x <= num_o else O # <= as X starts first

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves: set[tuple[int, int]] = set()
    for row_idx in range(3):
        for box_idx in range(3):
            if board[row_idx][box_idx] == EMPTY:
                possible_moves.add((row_idx, box_idx))

    logging.info(f"Possible moves: {possible_moves}")

    return possible_moves


def result(board, action) -> tuple[list[list[str]]]:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    logging.info(f"Finding result for action: {action}")
    if action is None:
        return copy.deepcopy(board)

    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Move has already been made")

    if action[0] not in range(3) or action[1] not in range(3):
        raise ValueError("Move is not valid")

    current_player = player(board)

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    logging.info(f"Finding if we have a winner...")

    # finvd vertical and horizontal wins
    for i in range(3):
        if (board[0][i] == board[1][i] == board[2][i] != EMPTY):
            return board[0][i]
        if (board[i][0] == board[i][1] == board[i][2] != EMPTY):
            return board[i][0]

    # find diagonal wins
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) or len(actions(board)) == 0:
       return True
    return False


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    logging.info(f"Calculating utility...")

    w = winner(board)
    if not w:
        return 0
    if w == X:
        return 1
    if w == O:
        return -1
    raise ValueError


def max_value(board, prev_action=None) -> tuple[int, Optional[Action]]:
    """
    Optimise for max value of X
    """
    logging.info(f"Finding best action for X...")
    value: int = -10000
    action_to_take: Optional[Action] = None
    if terminal(board):
        return utility(board), prev_action
    for action in actions(board):
        min_possible_result_from_action, _ = min_value(result(board, action), action)
        if min_possible_result_from_action > value:
            value = min_possible_result_from_action
            action_to_take = action
    return value, action_to_take

def min_value(board, prev_action=None) -> tuple[int, Optional[Action]]:
    """
    Optimise for min value of O
    """
    logging.info(f"Finding best action for O...")
    value: int = 10000
    action_to_take: Optional[Action] = None
    if terminal(board):
        return utility(board), prev_action
    for action in actions(board):
        max_possible_result_from_action, _ = max_value(result(board, action), action)
        if max_possible_result_from_action < value:
            value = max_possible_result_from_action
            action_to_take = action
    return value, action_to_take

def minimax(board) -> Optional[Action]:
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if current_player == X:
        return max_value(board)[1]
    elif current_player == O:
        return min_value(board)[1]

    else:
        raise ValueError


