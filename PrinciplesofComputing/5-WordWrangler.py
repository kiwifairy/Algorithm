"""
Student code for Word Wrangler game
http://www.codeskulptor.org/#user36_AIRyJXXz3A_18.py
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    lst = list1[:]
    for item in lst:
        tmp_list = lst[:]
        tmp_list.remove(item)
        for tmp in tmp_list:
            if item == tmp:
                lst.remove(tmp)
    return lst


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    ans_list = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                ans_list.append(item1)      
    return ans_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """   
    ans_list = []
    lst1 = list1[:]
    lst2 = list2[:]
    while lst1!=[] and lst2!=[]:
        if lst1[0]<lst2[0]:
            ans_list.append(lst1[0])
            lst1.remove(lst1[0])
        elif lst2[0]<lst1[0]:
            ans_list.append(lst2[0])
            lst2.remove(lst2[0])
        elif lst1[0]==lst2[0]:
            ans_list.append(lst1[0])
            ans_list.append(lst2[0])
            lst1.remove(lst1[0])
            lst2.remove(lst2[0])
    return ans_list+lst1+lst2
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 1 or len(list1) == 0:
        return list1
    else:
        new_list1 = list1[:len(list1)/2]
        new_list2 = list1[len(list1)/2:]
        merged_list = merge(merge_sort(new_list1),merge_sort(new_list2))
        return merged_list

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [word]
    first_char = word[0]
    rest_word = word[1:]
    joint_list = []
    rest_list = gen_all_strings(rest_word)
    for each_word in rest_list:
        for loc in range(-1,len(each_word)):
            new_word = each_word[:loc+1] + first_char + each_word[loc+1:]
            joint_list.append(new_word)    
    rest_list.extend(joint_list)
    return rest_list


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_list = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for item in netfile.readlines():
        word_list.append(item)
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
