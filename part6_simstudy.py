from statistictests import ChiSquare
import numpy

"""
This file should be used to keep all necessary code that is used for the verification section in part 6
of the programming assignment. It contains task 6.2.1.
"""


def task_6_2_1():
    """
    This task is used to verify the implementation of the chi square test.
    First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
    whether they follow the original or another given distribution.
    """
    # TODO Task 6.2.1: Your code goes here
    x = []
    for i in range(100):
        xi = 0
        xi = numpy.random.normal(0, 1)
        x.append(xi)

    bins = 15
    emp_n, emp_x = numpy.histogram(x, bins=bins)
    Ch_2 = ChiSquare(emp_x, emp_n)
    Ch_2.test_distribution(0.05, 0, 1)
    # pass


if __name__ == '__main__':
    task_6_2_1()
