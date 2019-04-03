# coding: utf-8
# start at 19:09

from string import *

def countSubStringMatch(target,key):
    target_begin = target

    count = 0
    index_ = find(target_begin, key)
    while index_ != -1:
        target_begin = target_begin[index_ + 1:]
        index_ = find(target_begin, key, index_+1)
        count += 1
    return count

def countSubStringMatchRecursive (target, key):
    target_begin = target

    count = 0
    index_ = find(target_begin, key)
    if index_ != -1:
        target_begin = target_begin[index_+1:]
        count += 1

        count += countSubStringMatchRecursive(target_begin, key)
    return count


def testA():
    print countSubStringMatch("atgacatgcacaagtatgcat", "atgc")
    print countSubStringMatchRecursive("atgacatgcacaagtatgcat", "atgc")

testA()

# cost about 16 minutes

