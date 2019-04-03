# coding: utf-8
# problem 1

def desired_match(desired_num, combination):
    a = combination[0]
    b = combination[1]
    c = combination[2]

    i = 0
    while (a*i) <= desired_num:
        j = 0
        while (a * i + b * j) <= desired_num:
            k = 0
            while (a * i + b * j + c * k) <= desired_num:
                if (a * i + b * j + c * k) == desired_num:
                    # print i, j, k, 'Target:', desired_num
                    return True
                k += 1
            j += 1
        i += 1
    return False

def testA():
    combination = [6, 9, 20]
    desire_list = [50, 51, 52, 53, 54, 55]
    result = []
    for each in desire_list:
        result.append(desired_match(each, combination))
    print(desire_list)
    print(result)
    pass_num = sum(result)
    if pass_num == len(desire_list):
        print 'All True'
    else:
        print 'Failed num:', len(desire_list) - pass_num


def testB():
    combination = [6, 9, 20]
    desire_list = [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
    result = []
    for each in desire_list:
        result.append(desired_match(each, combination))
    print(desire_list)
    print(result)
    pass_num = sum(result)
    if pass_num == len(desire_list):
        print 'All True'
    else:
        print 'Failed num:', len(desire_list) - pass_num

# testA()
# testB()
# cost time about 20 minutes


# problem set 2
# 实在没想出来怎么证明
# Answer: For this type of problem, if you can find a string of sequential numbers that
# is as long as the smallest counting unit then you can count to any subsequent number
# by adding this smallest counting unit a member of this base sequential series.Wow.


# problem set 3
def test_ps2a():
    combination = [6, 9, 20]

    start_num = 0
    all_true = False
    while not all_true:
        count = 0
        for i in xrange(start_num, start_num+6):
            if desired_match(i, combination):
                count += 1
        if count == 6:
            print 'Largest number of McNuggets that cannot be bought in exact quantity: <%d>' % (start_num-1)
            break
        start_num += 1

test_ps2a()

# problem 3---cost about 10 minutes



###
### template of code for Problem 4 of Problem Set 2, Fall 2008
###

bestSoFar = 0     # variable that keeps track of largest number
                  # of McNuggets that cannot be bought in exact quantity
packages = (6,9,20)   # variable that contains package sizes

for n in range(1, 150):   # only search for solutions up to size 150
    ## complete code here to find largest size that cannot be bought
    ## when done, your answer should be bound to bestSoFar
    if not desired_match(n, packages):
        print 'Givenpackage sizes <%d>, <%d>, and <%d>, ' \
              'the largest number of McNuggets that cannot ' \
              'be bought in exact quantity is: <%d>' \
              % (packages[0], packages[1], packages[2], n)

# cost about 10 minutes