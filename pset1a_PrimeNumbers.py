# coding: utf-8
import math

primes_dict = {}

# def generate_dividend(num):
#     odd_list = []
#     actual_range = int(math.ceil(math.sqrt(num)))
#     # print('expected: [1,', actual_range, '] actual:', xrange(1, actual_range+1))
#     for i in xrange(2, actual_range+1):
#             odd_list.append(i)
#     # print(odd_list)
#     return odd_list
#
# def is_prime(num):
#     odd_list = generate_dividend(num)
#     if len(odd_list) == 0:
#         return False
#     # print("Entering...for")
#     for odd in odd_list:
#         if num == odd:
#             continue
#         if num % odd == 0:
#             return False
#     return True
def is_prime(n):
    if n == 1:
        return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def get_primes(index):
    result = []
    test_num = 0
    count_time = 0
    while count_time < index:
        test_num += 1
        # if count_time in primes_dict:
        #     count_time += 1
        #     continue

        if is_prime(test_num):
            # primes_dict[count_time] = test_num
            result.append(test_num)
            count_time += 1
            # print(test_num, " ")
        # print(test_num, " is testing!")
    return result

def get_ith_prime(index):
    return get_primes(index)[-1]

def testA_single():
    print is_prime(1), ", Expected: False"
    print is_prime(2), ", Expected: True"
    print is_prime(3), ", Expected: True"
    print is_prime(4), ", Expected: False"
    print is_prime(5), " Expected: True"

def testB():
    print("Actual:", get_ith_prime(5), "Expected: 11")


# testA_single()
# testB()

# print 'result:', get_ith_prime(6000)
##########################################
# the code up there cost about 50 minutes
##########################################

# part 2
# 数论：第n个素数p的指数e**p，与前n个（包括）素数的积的比值总小于或约等于1

def test_logarithm_to_prime(times):
    result = get_primes(times)
    Nth_result = result[-1]
    for index in xrange(len(result)):
        result[index] = math.log(result[index])
    total_sum = sum(result)
    print('Nth:', Nth_result, '  ', total_sum, ' ratio:', total_sum/Nth_result)

test_logarithm_to_prime(6000)

##########################################
# the code up there cost about 60 minutes, including understand the subject
##########################################
