import tictactoe as ttt

def test_one_action_to_win():
    board = [[ttt.X, ttt.X, ttt.O],
             [ttt.O, ttt.X,  ttt.X],
             [ttt.O,  None,  ttt.O]]
    _, a = ttt.max_value(board, None)

    if a is None:
        assert False
    assert a == (2, 1)

