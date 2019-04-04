# coding: utf-8
# start at 19:34
import math

def nestEggFixed(salary, save, growth_rate, work_year):
    result = []
    end_sum = 0
    for i in xrange(work_year):
        end_sum = end_sum*(1+0.01*growth_rate) + salary*save*0.01
        result.append(end_sum)
    return result

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]

# testNestEggFixed()

#
# Problem 2
#

def nestEggVariable(salary, save, growth_rate):
    # TODO: Your code here.
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: a list of the annual percent increases in your investment
      account (integers between 0 and 100).
    - return: a list of your retirement account value at the end of each year.
    """
    result = []
    end_sum = 0
    for i in xrange(len(growth_rate)):
        end_sum = end_sum * (1 + 0.01 * growth_rate[i]) + salary * save * 0.01
        result.append(end_sum)
    return result

def testNestEggVariable():
    salary = 10000
    save = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]

    # TODO: Add more test cases here.

# testNestEggVariable()

#
# Problem 3
#

def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    remained = []
    first_sum = savings
    for i in xrange(len(growthRates)):
        first_sum = first_sum*(1+0.01*growthRates[i]) - expenses
        remained.append(first_sum)
    return remained


def testPostRetirement():
    savings     = 100000
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 30000
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print savingsRecord
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]

    # TODO: Add more test cases here.

# testPostRetirement()


#
# Problem 4
#

def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """
    savings = nestEggVariable(salary, save, preRetireGrowthRates)
    latest_saving = savings[-1]

    expense_up = latest_saving
    expense_down = 0
    expenses_ = (expense_up + expense_down)/2.0

    for i in range(0, 1000):
        remained_fund = postRetirement(latest_saving, postRetireGrowthRates, expenses_)
        latest_fund = remained_fund[-1]
        if latest_fund > epsilon: # 取少了
            expense_down = (expense_down+expense_up)/2.0
            # expense_up = latest_saving
        elif latest_fund < 0 and latest_fund < epsilon:
            expense_up = (expense_down + expense_up) / 2.0
            # expense_down =
        expenses_ = (expense_up+expense_down)/2.0

    return  expenses_

def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print expenses
    # Output should have a value close to:
    # 1229.95548986

testFindMaxExpenses()

# cost totally about 45 minutes

