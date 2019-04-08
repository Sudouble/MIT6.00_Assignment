# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    result = {}
    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    for line in inputFile:
        line_list = line.strip().split(',')
        name = line_list[0]
        value = line_list[1]
        work = line_list[2]
        # print line
        result.setdefault(name, (int(value), int(work)))
    return result

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

# subjects = loadSubjects(SUBJECT_FILENAME)
# printSubjects(subjects)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    remainWork = maxWork
    result = dict()

    for key, subInfo in subjects.items():
        tmpKey = key
        tempMax = subInfo
        # print('start:', remainWork, ' key:', tmpKey, ' sub:', tempMax)
        for key1, subInfo1 in subjects.items():
            if key == key1 or key in result or key1 in result:
                continue
            if not comparator(subInfo, subInfo1):
                tmpKey = key1
                tempMax = subInfo1
        #     print('remainWork:', remainWork, ' key:', tmpKey, ' sub:', tempMax)
        # print("Next Round.")

        remainWork -= tempMax[WORK]
        # print('remainWork:', remainWork, ' key:', tmpKey, ' sub:', tempMax)
        if remainWork < 0:
            break
        result.setdefault(tmpKey, tempMax)

    return result

def testGreedyAdvisor():
    subjects = { '6.00': (16, 8),
                 '1.00': (7, 7),
                 '6.01': (5, 3),
                 '15.01': (9, 6)}
    printSubjects(greedyAdvisor(subjects, 15, cmpValue))
    print '{\'6.00\': (16, 8), \'15.01\': (9, 6)}'

    printSubjects(greedyAdvisor(subjects, 15, cmpWork))
    print '{\'6.01\': (5, 3), \'15.01\': (9, 6)}'

    printSubjects(greedyAdvisor(subjects, 15, cmpRatio))
    print '{\'6.00\': (16, 8), \'6.01\': (5, 3)}'

# testGreedyAdvisor()


def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = subjects.keys()
    tupleList = subjects.values()
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    # TODO...
    subjects = loadSubjects(SUBJECT_FILENAME)
    start = time.time()
    bruteForceAdvisor(subjects, 9)
    end = time.time()
    print 'Duration: ', end - start, ' s'

# bruteForceTime()

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance
# work 3, time 0.021999835968017578 s
# work 4, time 0.0789999961853 s
# work 5, time 0.37700009346 s
# work 6, time 0.840000152588 s
# work 7, time 2.66199994087 s
# work 8, time 6.70499992371 s
# work 9, time 17.771999836 s
#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    nameList = subjects.keys()
    tupleList = subjects.values()
    weights = [singles[WORK] for singles in tupleList]
    values = [singles[VALUE] for singles in tupleList]
    memos = {}
    bestSubset, bestSubsetValue = \
        bruteForceAdvisorHelperFast(weights, values, 0, maxWork, memos)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects


def bruteForceAdvisorHelperFast(weights, values, i, maxwork, memos):
    # print '-------', i, maxwork
    if i >= len(weights)-1:
        if maxwork <= 0:
            return [], 0
        return [i], values[i]

    key = (i, maxwork)
    if key in memos:
        return memos[key]

    tmp_i1, value1 = bruteForceAdvisorHelperFast(weights, values, i + 1, maxwork, memos)
    if weights[i] > maxwork:
        memos[key] = tmp_i1, value1
        return tmp_i1, value1
    else:
        tmp_i2, value2 = bruteForceAdvisorHelperFast(weights, values, i+1, maxwork-weights[i], memos)
        total_v = (value2 + values[i])
        if total_v > value1:
            memos[key] = [i] + tmp_i2, total_v
            return [i] + tmp_i2, total_v
        else:
            memos[key] = tmp_i1, value1
            return tmp_i1, value1

#
# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    # TODO...
    subjects = loadSubjects(SUBJECT_FILENAME)
    start = time.time()
    dpAdvisor(subjects, 90)
    end = time.time()
    print 'Duration: ', end - start, ' s'

# dpTime()

subjects = loadSubjects(SUBJECT_FILENAME)

max_work = 30
# printSubjects(bruteForceAdvisor(subjects, max_work))
printSubjects(dpAdvisor(subjects, max_work))

# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.
# really fast with dynamic programming, because we eliminate the duplicate calc.
# 从子问题出发，一直推广到N个情况

# total coust about 3 hours