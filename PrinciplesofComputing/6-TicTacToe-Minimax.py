"""
Mini-max Tic-Tac-Toe Player
http://www.codeskulptor.org/#user36_r7VrqlAqVc_22.py
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import poc_tree

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    result = board.check_win()  # get result of the current board
    if result == None:
        move_list = board.get_empty_squares()  # get the tree branches and possible next moves
        best = (None, (-1, -1))
        for step in move_list:
            bd_clone = board.clone()
            bd_clone.move(step[0], step[1], player)   #make a move on a cloned board
            next_player = provided.switch_player(player)
            next_score = mm_move(bd_clone, next_player)  #make a recursive call to mm_move() pasing the cloned board and the 'other' player
            if player == 3: #if it is oppo O--min
                if best[0] == None or (next_score[0] < best[0]):
                    best = (next_score[0], step)
                    #print best
            elif player ==2: #if it is X--max
                if best[0] == None or (next_score[0] > best[0]):
                    best = (next_score[0], step)
        return best
    else:
        return SCORES[result], (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]
#a=mm_move(provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERO, provided.PLAYERX]]), provided.PLAYERX)
#a = mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX )
#a = mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#a = mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#print a, type(a)
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
