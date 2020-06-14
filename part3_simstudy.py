from rng import ExponentialRNS, UniformRNS
from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
import time

"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""

def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    rns_exp = ExponentialRNS(1, the_seed=0)
    rns_uni = UniformRNS(1, 100, the_seed=0)
    n = 10000

    exp_distr = []
    uni_distr = []
    weights = []

    for _ in range(n):
        exp_distr.append(rns_exp.next())
        uni_distr.append(rns_uni.next())
        weights.append(1./float(n))

    pyplot.subplot(121)
    pyplot.hist(exp_distr, bins=30, weights=weights,  edgecolor='black')
    pyplot.xlabel("x")
    pyplot.ylabel("distribution over n")
    pyplot.title("Exponential distribution")

    pyplot.subplot(122)
    pyplot.hist(uni_distr, bins=30, weights=weights,  edgecolor='black')
    pyplot.xlabel("x")
    pyplot.ylabel("distribution over n")
    pyplot.title("Uniform distribution")

    pyplot.show()


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    sim = Simulation()
    cnt = TimeIndependentCounter("sys_util")
    sim.sim_param.S = 5

    sim.sim_param.SIM_TIME = 100000
    print('Results for simulation time of 100s')
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        cnt.reset()
        for _ in range(100):
            cnt.count(sim.do_simulation().system_utilization)
        print('rho = %s, real system utilization/throughput = %.4f' % (rho, cnt.get_mean()))

    sim.sim_param.SIM_TIME = 1000000
    print('\nResults for simulation time of 1000s')
    for rho in [0.01, 0.5, 0.8, 0.9]:
        sim.sim_param.RHO = rho
        sim.reset()
        cnt.reset()
        for _ in range(100):
            cnt.count(sim.do_simulation().system_utilization)
        print("rho = %s, real system utilization/throughput = %.4f" % (rho, cnt.get_mean()))


if __name__ == '__main__':
    # task_3_2_1()
    task_3_2_2()
