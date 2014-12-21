"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
http://www.codeskulptor.org/#user35_xDLbv3S5gn_8.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    hand: full yahtzee hand
    Returns an integer score
    """
    score_list = []
    hd_set = set(hand)
    for item in hd_set:
        score_list.append(hand.count(item)*item)
    return max(score_list)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    total_score = 0.0
    random_set = set([()])
    full_possibility_list = []
    die_outcome = [num+1 for num in range(num_die_sides)]
    random_set = gen_all_sequences(die_outcome, num_free_dice)  # generate the random set of the free dice
    for pos in random_set:  
        full_possibility_list.append(list(pos))  # convert the element(original tuple) in random_set into list
    held_dice_list = list(held_dice)
    for item in full_possibility_list: # generate the full possible list: free_dice +  held_dice
        item.extend(held_dice_list)
    for tmp in full_possibility_list: # count the score of each full_set element
        total_score += score(tmp)
    return total_score/(num_die_sides**num_free_dice)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    if not hand:
        return set([()])
    last_ele = hand[-1]
    hand = hand[:-1]
    joint_set = set()
    for partial_sequence in gen_all_holds(hand):
        new_sequence = list(partial_sequence)
        new_sequence.append(last_ele)
        joint_set.add(tuple(new_sequence))    #joint_set = gen_all_holds(hand)+last_ele
    result_set = gen_all_holds(hand).union(joint_set)
    return result_set
    #[[first_item_in_hand] + next_recursion_step_result] + next_recursion_step_result

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_hold = gen_all_holds(hand)
    result_pair = {}
    value = 0
    for item in possible_hold:
        value = expected_value(item, num_die_sides, len(hand)-len(item))
        result_pair[value] = item 
    return (max(result_pair), result_pair[max(result_pair)] )


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    #hand = (1,)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
   
   
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                      