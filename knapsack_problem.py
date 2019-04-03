# coding: utf
import math

w = [5, 3, 2]
v = [9, 9, 8]
length = len(w)

value = 0
num_calls = 0


def max_val(w, v, left_item, left_pound, memo):
    global num_calls
    num_calls = num_calls + 1
    print "item:", left_item, " pound:", left_pound
    try:
        return memo[(left_item, left_pound)]
    except KeyError:
        if left_item == 0 or left_pound == 0:
            return 0
        if w[left_item-1] > left_pound:
            return max_val(w, v, left_item - 1, left_pound, memo)
        else:
            res = max(max_val(w, v, left_item-1, left_pound, memo),
                            v[left_item-1] + max_val(w, v, left_item-1, left_pound-w[left_item-1], memo))
            memo[(left_item, left_pound)] = res
            return res


w = [1, 1, 5, 5, 3, 3, 4, 4]
v = [15, 15, 10, 10, 9, 9, 5, 5]
memo = {}
print max_val(w, v, 3, 5, memo), ' calls:', num_calls
