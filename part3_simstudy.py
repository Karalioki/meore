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
    uni = UniformRNS(0, 5)
    exp = ExponentialRNS(5)
    expArray = []
    uniArray = []
    n = 10000
    bin_number = int(numpy.sqrt(n) / 2) 
    weights = [1.0 / n] * n

    for _ in range(n):
        expArray.append(uni.next())
        uniArray.append(exp.next())

    pyplot.subplot(121)
    pyplot.hist(expArray, bins=bin_number, weights=weights)
    pyplot.subplot(122)
    pyplot.hist(uniArray, bins=bin_number, weights=weights)
    pyplot.show()


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    def print_array(arr):
        for val in arr:
            print(val[0], val[1])
        print()

    def get_util_values(sim):
        rho_values = [0.01, 0.5, 0.8, 0.9]
        system_util_values = []
        for rho_value in rho_values:
            sim.sim_param.RHO = rho_value
            sim.reset()
            sim.do_simulation()
            system_util_values.append(('rho=' + str(rho_value), 'system utilization=' + str(sim.sim_result.system_utilization)))
        return system_util_values

    sim = Simulation()
    sim.sim_param.S = 5
    sim.sim_param.SIM_TIME = 100000

    system_util_values = get_util_values(sim)
    print("For t=100s system utilization values are:")
    print_array(system_util_values)

    sim.sim_param.SIM_TIME = 1000000
    system_util_values = get_util_values(sim)
    print("For t=1000s system utilization values are:")
    print_array(system_util_values)

if __name__ == '__main__':
    task_3_2_1()
    task_3_2_2()
