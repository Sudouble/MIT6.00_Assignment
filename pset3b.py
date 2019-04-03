# coding: utf-8

from string import *

# problem 2

def subStringMatchExact(target, key):
    target_begin = target

    result = []
    index_ = find(target_begin, key)
    while index_ != -1:
        result.append(index_)
        # print(index_, target_begin)
        index_ = find(target_begin, key, index_+1)
    return tuple(result)


def testA():
    target1 = 'atgacatgcacaagtatgcat'
    target2 = 'atgaatgcatggatgtaaatgcag'
    key10 = 'a'
    key11 = 'atg'
    key12 = 'atgc'
    key13 = 'atgca'
    print subStringMatchExact(target1, key11)

    targets = [target1, target2]
    keys = [key10, key11, key12, key13]
    for target in targets:
        for key in keys:
            result = subStringMatchExact(target, key)
            print 'Target:', target, ', Key:', key, ', Result:', result

# testA()

