# Problem Set 5: Ghost
# Name: 
# Collaborators: 
# Time: 
#

import random
# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

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

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

# TO DO: your code begins here!
def is_valid_word(word, word_list, RULED_LENGTH):
    word = word.lower()
    for each_word in word_list:
        if word == each_word[:len(word)]:
            if len(word) < RULED_LENGTH:
                return 1
            elif len(word) == RULED_LENGTH:
                return 2
            elif word == each_word:
                return 4
            else:
                return 3
    return 0

def test_valid_word():
    word = 'a'
    print is_valid_word(word, wordlist, 3)

    word = 'M'
    print is_valid_word(word, wordlist, 3)

    word = 'cat'
    print is_valid_word(word, wordlist, 3)

    word = 'catsdfew'
    print is_valid_word(word, wordlist, 3)
# test_valid_word()

def gen_players(N):
    return [i+1 for i in range(N)]

def get_one_word(each):
    while True:
        print 'Player %s\'s turn.' % each
        strTmp = "Player %s says letter:" % each
        input_char = raw_input(strTmp)
        if len(input_char) != 1 or (input_char not in string.ascii_letters):
            continue
        else:
            return input_char.upper()

def output_result(word, each, players):
    print 'Player %s loses because \'%s\' is not a word!' % (each, word)
    print 'Player ', [i for i in players if i != each], ' wins!'

def ghost():
    print 'Welcome to Ghost!'
    word = ''

    players = gen_players(2)
    print 'Player %s goes first.' % (players[0])
    print
    print 'Current word fragment: \'%s\'' % word
    while True:
        for each in players:
            word += get_one_word(each)
            print 'Current word fragment: \'%s\'' % word

            RULED_LENGTH = 3
            result = is_valid_word(word, wordlist, RULED_LENGTH)
            if result == 1 or result == 3:
                continue
            elif result == 2:
                print 'Player %s has formed the word %s, but that\'s okay' \
                      'because it is not longer than %s letters' % (each, word, RULED_LENGTH)
            elif result == 4:
                print 'Player %s loses because \'%s\' is a word!' % (each, word)
                print 'Player ', [i for i in players if i != each], ' wins!'
                return
            else:
                output_result(word, each, players)
                return

ghost()

