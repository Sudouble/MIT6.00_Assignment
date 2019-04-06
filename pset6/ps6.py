# Problem Set 5: 6.00 Word Game
# Name: 
# Collaborators: 
# Time: 
#

import random
import copy
import time
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO ...
    sum_ = 0
    for each in word:
        sum_ += SCRABBLE_LETTER_VALUES[each]
    if n == len(word):
        sum_ += 50
    return sum_

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,              # print all on the same line
    print                              # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_tmp = {}
    hand_tmp = hand
    for each in word:
        hand_tmp[each] = hand_tmp.get(each, 0) - 1
    return hand_tmp
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # print(word, hand)
    hand_tmp = copy.deepcopy(hand)
    for each in word:
        if hand_tmp.get(each, 0) == 0:
            return False
        if hand_tmp.get(each, 0) != 0:
            hand_tmp[each] = hand_tmp.get(each) - 1
        # print(hand_tmp)
    if word not in word_list:
        return False
    return True


def get_word_rearrangements(a_list_of_words):
    """
    This function takes a list of words and returns a dictionary of strings mapped to actual words.

    This function is used by the computer-player to find valid words.

    Create a dict where, for any set of letters, you can determine if there is some acceptable word that is a rearrangement of those letters.
    Let d = {}
    For every word w in the word list:
        Let d[(string containing the letters of w in sorted order)] = w
    """
    rearrange_dict = {}
    for word in a_list_of_words:
        #   build a list from the char in word: 1) convert word string to list, 2) sort list, 3) convert list back to string.
        char_list = []
        my_string = ''
        for char in word:
            char_list.append(char)
        char_list.sort()
        for each in range(len(char_list)):
            my_string += char_list[each]
        rearrange_dict[my_string] = word
    # print "In get_word_rearrangements. Rrearrange_dict:", rearrange_dict
    return rearrange_dict

def get_words_to_points(word_list):
    """
     Return a dict that maps every word in word_list to its point value.
     """
    dict_result = {}
    for each_word in word_list:
        score = get_word_score(each_word, HAND_SIZE)
        dict_result.setdefault(each_word, score)
    return dict_result


def is_valid_word_robot(word, hand):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # print(word, hand)
    hand_tmp = copy.deepcopy(hand)
    for each in word:
        if hand_tmp.get(each, 0) == 0:
            return False
        if hand_tmp.get(each, 0) != 0:
            hand_tmp[each] = hand_tmp.get(each) - 1
        # print(hand_tmp)
    return True


def pick_best_word(hand, points_dict):
    """
    Return the highest scoring word from points_dict that can be made with the
    given hand.
    Return '.' if no words can be made with the given hand.
    """
    word = ''
    point_score = 0
    for word_, point in points_dict.items():
        if is_valid_word_robot(word_, hand):
            if point_score < point:
                point_score = point
                word = word_
    return word


def get_time_limit(points_dict, k):
    """
     Return the time limit for the computer player as a function of the
    multiplier k.
     points_dict should be the same dictionary that is created by
    get_words_to_points.
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    end_time = time.time()
    return (end_time - start_time) * k


def build_substrings(string):
    """
    Works on the premiss that given a set of the substrings of a string the
    the subsets of a string with one more char is the formed by taking all the
    substrings in the known subset and also adding to them the set formed by
    adding the character to every element in the old set and then adding the
    new char.

    """
    result = []
    if len(string) == 1:
        result.append(string)
    else:
        for substring in build_substrings(string[:-1]):
            result.append(substring)
            substring = substring + string[-1]
            result.append(substring)
        result.append(string[-1])
        result = list(set(result))  # Convert result into a set.  Sets have no duplicates. Then convert back to list.
        result.sort()
    # now iterate through substrings and sort the characters of each substring
    # for each in
    return result

def sort_word(word_string):
    """
    Takes a string, alphabetizes it and returns it as a string.
    """
    char_list =[]
    sorted_string = ''
    for char in word_string:
        char_list.append(char)
    char_list.sort()
    for char in char_list:
        sorted_string += char
    return sorted_string

def pick_best_word_faster(hand, rearrange_dict):
    """
    Takes a hand {dictionary} and a dictionary of letter combinations that map to a valid word.

    Returns the highest value word or '.'-if there is no valid word possible.

    Pseudo-code:
    To find some word that can be made out of the letters in HAND:
        For each subset S of the letters of HAND:
            Let w = (string containing the letters of S in sorted order)
            If w in d:
                return d[w]

    This function must convert the hand{dictionary} to a string.  In doing so it must check to make sure that the value of each key in the had is > 0
    """
    # print "In pick best. Hand:", hand
    hand_string = ''

    for each in hand:
        if hand[each] > 0:
            hand_string += each * hand[each]

    # print "Hand sorted: %s" %hand_string

    best_word = ''
    best_word_score = 0
    subsets = build_substrings(hand_string)
    subset_value = 0

    for subset in subsets:
        sorted_subset = sort_word(subset)
        if sorted_subset in rearrange_dict:
            subset_value = get_word_score(sorted_subset, HAND_SIZE)
            if subset_value > best_word_score:
                best_word = rearrange_dict[sorted_subset]
                best_word_score = subset_value

    if best_word_score > 0:
        return best_word
    else:
        return '.'

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    due_time = 8  # second
    remain_time = due_time
    sum = 0
    while True:
        display_hand(hand)
        begin_time = time.time()
        word = raw_input("Enter word, or a . to indicate that you are finished:")
        end_time = time.time()

        duration = end_time - begin_time
        remain_time -= duration
        if remain_time < 0:
            remain_time = 0
        print 'It took %s seconds to provide an answer.' % duration
        print 'You have %s seconds remaining' % remain_time
        if remain_time <= 0:
            break

        if word == '.':
            break
        if not is_valid_word(word, hand, word_list):
            print('Rejected.')
            continue
        hand = update_hand(hand, word)
        score = get_word_score(word, HAND_SIZE)
        sum += score/(duration)
        print 'He earned ', score, '. Total:', sum, ' points'
    # print 'Total score:', sum, ' points.'
    print 'Total time exceeds %s seconds. You scored %s points.' % (due_time, sum)


def play_hand_v2(hand, word_list):
    word_points = get_words_to_points(word_list)
    due_time = get_time_limit(word_points, 20)  # second
    remain_time = due_time
    sum = 0
    while True:
        display_hand(hand)
        begin_time = time.time()
        # word = raw_input("Enter word, or a . to indicate that you are finished:")
        word = pick_best_word(hand, word_points)
        if word == '':
            break
        print word
        end_time = time.time()

        duration = end_time - begin_time
        remain_time -= duration
        if remain_time < 0:
            remain_time = 0
        print 'It took %d seconds to provide an answer.' % duration
        print 'You have %d seconds remaining' % remain_time
        if remain_time <= 0:
            break

        if word == '.':
            break
        if not is_valid_word(word, hand, word_list):
            print('Rejected.')
            continue
        hand = update_hand(hand, word)
        score = get_word_score(word, HAND_SIZE)
        sum += score / duration
        print 'He earned ', score, '. Total:', sum, ' points'
    # print 'Total score:', sum, ' points.'
    print 'Total time exceeds %s seconds. You scored %s points.' % (due_time, sum)


def play_hand_v3(hand, word_list):
    word_points = get_words_to_points(word_list)
    rearrange_dict = get_word_rearrangements(word_list)
    due_time = get_time_limit(word_points, 20)  # second
    remain_time = due_time
    sum = 0
    while True:
        display_hand(hand)
        begin_time = time.time()
        # word = raw_input("Enter word, or a . to indicate that you are finished:")
        word = pick_best_word_faster(hand, rearrange_dict)
        if word == '':
            break
        print word
        end_time = time.time()

        duration = end_time - begin_time
        remain_time -= duration
        if remain_time < 0:
            remain_time = 0
        print 'It took %d seconds to provide an answer.' % duration
        print 'You have %d seconds remaining' % remain_time
        if remain_time <= 0:
            break

        if word == '.':
            break
        if not is_valid_word(word, hand, word_list):
            print('Rejected.')
            continue
        hand = update_hand(hand, word)
        score = get_word_score(word, HAND_SIZE)
        sum += score / (duration+0.1)
        print 'He earned ', score, '. Total:', sum, ' points'
    # print 'Total score:', sum, ' points.'
    print 'Total time exceeds %s seconds. You scored %s points.' % (due_time, sum)


#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO ...
    # print "play_game not implemented."          # delete this once you've completed Problem #4
    # play_hand(deal_hand(HAND_SIZE), word_list)  # delete this once you've completed Problem #4
    
    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE)  # random init
    while True:
       cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
       if cmd == 'n':
           hand = deal_hand(HAND_SIZE)
           # play_hand(hand.copy(), word_list)
           # play_hand_v2(hand.copy(), word_list)
           play_hand_v3(hand.copy(), word_list)
           print
       elif cmd == 'r':
           # play_hand(hand.copy(), word_list)
           # play_hand_v2(hand.copy(), word_list)
           play_hand_v3(hand.copy(), word_list)
           print
       elif cmd == 'e':
           break
       else:
           print "Invalid command."

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

# problem 1&2 about 20 minutes

# problem 5 analysis:
# pick_best_word(...)---> O(N*m) N is the size of dict, m is the size of hand
# pick_best_word_fast(...)---> O(logN*m!) N is the size of dict, m is the size of hand

