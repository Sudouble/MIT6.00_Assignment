
from string import *
from pset3b import subStringMatchExact
from pset3c import subStringMatchOneSub

# these are some example strings for use in testing your code

#  target strings
target1 = 'atgacatgcacaagtatgcat'
target2 = 'atgaatgcatggatgtaaatgcag'

# key strings
key10 = 'a'
key11 = 'atg'
key12 = 'atgc'
key13 = 'atgca'

def subStringMatchExactlyOneSub(target,key):
    """
    This function takes two arguments: a target string and a key string.

    It returns a tuple of all starting points of matches of the key to the target, such that at exactly one element of the key is incorrectly matched to the target.
    """
    possible_answer = subStringMatchOneSub(key, target)
    answer = possible_answer
    perfect_matches = subStringMatchExact(target, key)
    to_remove_from_answer = ()
    # this for loop identifies the positions in possible_answer that contain perfect matches.
    for i in range(0, len(possible_answer)):
        for j in range(0, len(perfect_matches)):
            if possible_answer[i] == perfect_matches[j]:
                # print "matches:", possible_answer[i]
                to_remove_from_answer += (i,)
            # print to_remove_from_answer

    # this for loop removes the items from the possible_answer tuple begin at the end and working forward.
    for m in reversed(to_remove_from_answer):
        # print to_remove_from_answer[-m]
        # print m
        answer = answer[:m] + answer[m + 1:]
    # print answer
    return answer


def testA():
    targets = [target1, target2]
    keys = [key10, key11, key12, key13]
    for target in targets:
        for key in keys:
            result = subStringMatchExactlyOneSub(target, key)
            print 'Target:', target, ', Key:', key, ', Result:', result

testA()

# cost about 40 minutes, including reading
