from matplotlib import pyplot
from rng import ExponentialRNS, UniformRNS
import numpy
from simulation import Simulation
from simparam import SimParam
"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""


def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.


    Generate a sufficient number
of samples by using the classes RNG and/or RNS and choose a reasonable number of bins for
your histograms.
    """
    # TODO Task 3.2.1: Your code goes here
    sim = Simulation()
    uni = sim.rng.UniformRNS(0, 5)
    exp = sim.rng.ExponentialRNS(5)
    expArray = []
    uniArray = []
    n = 100
    for i in n:
        expArray.append(uni())
        uniArray.append(exp())

    pyplot.subplot(121)
    pyplot.hist(expArray, bins=10)
    pyplot.subplot(122)
    pyplot.hist(uniArray, bins=10)
    pyplot.show()


    pass


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 5
    sim.sim_param.SIM_TIME = 100000
    rho = [0.01, 0.5, 0.8, 0.9]
    for i in rho:
        sim.sim_param.RHO = i
        sim.reset()
        sim.do_simulation()
    sim.sim_result.system_utilization()
    pass


if __name__ == '__main__':
    task_3_2_1()
    task_3_2_2()
