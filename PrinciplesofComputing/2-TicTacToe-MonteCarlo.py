"""
Monte Carlo Tic-Tac-Toe Player
http://www.codeskulptor.org/#user35_mqr8syjmeL_12.py
"""
import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 1    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 2.0  # Score for squares played by the other player
  
# Add your functions here.
def mc_trial(board, player):
    """
    play a game starting with the given player by making random moves, 
    alternating between players. 
    """
    while board.check_win()== None:
        empty = board.get_empty_squares()
        random_move = random.choice(empty)
        board.move(random_move[0], random_move[1], player)        
        player = provided.switch_player(player)
   
def mc_update_scores(scores, board, player):
    """
    score the completed board and update the scores grid. 
    """
    x_score = 0
    o_score = 0
    x_value = 0
    o_value = 0
    dim = board.get_dim()
    winner = board.check_win()
    if player == 3 :
        o_value = MCMATCH
        x_value = MCOTHER
    elif player == 2 :
        x_value = MCMATCH
        o_value = MCOTHER
    if winner == 2 :
        x_score = 1
        o_score = -1
    elif winner == 3 :
        x_score = -1
        o_score = 1
    for row in range(dim):
        for col in range(dim):
            status = board.square(row, col)
            if status == 2:
                scores[row][col] += x_score * x_value
            elif status == 3 :
                scores[row][col] += o_score * o_value
            elif status == 1 :
                scores[row][col] += 0
                
def get_best_move(board, scores):
    """
     find all of the empty squares with the maximum score 
     randomly return one of them as a (row, column) tuple.
    """
    empty_list = board.get_empty_squares()
    score_list = []
    max_list = []
    if len(empty_list)==0:
        return None
    else:
        for tmp in empty_list:
            score_list.append(scores[tmp[0]][tmp[1]])
        for tmp2 in empty_list:
            if scores[tmp2[0]][tmp2[1]] == max(score_list):
                max_list.append(tmp2)
        return random.choice(max_list)
    
def mc_move(board, player, trials):
    """
    use the Monte Carlo simulation 
    to return a move for the machine player 
    in the form of a (row, column) tuple. 
    """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)]for dummyrow in range(dim)]
    trial_times = trials*10
    while trial_times >0:
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
        trial_times -= 1
    nxt=get_best_move(board, scores)
    return nxt
   
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)      
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)