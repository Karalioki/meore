from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation
from packet import Packet
import matplotlib.pyplot as plt
import numpy as np
"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    # autocor = TimeIndependentAutocorrelationCounter(max_lag=5)
    # for i in range(5000):
    #     autocor.count(1)
    #     autocor.count(-1)
    # autocor.report()
    #
    # autocor.reset()
    # for i in range(5000):
    #     autocor.count(1)
    #     autocor.count(1)
    #     autocor.count(-1)
    # autocor.report()
    pass


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    # sim = Simulation()
    # sim.sim_param.S = 10000
    # sim.sim_param.SIM_TIME = 10000000
    # rho = [0.01, 0.5, 0.8, 0.95]
    # for i in rho:
    #     sim.sim_param.RHO = i
    #     sim.reset()
    #     sim.do_simulation()
    #     sim.counter_collection.report()
    pass




def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    # TODO Task 4.3.2: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000
    rho = [0.01, 0.5, 0.8, 0.95]
    packet = Packet(sim)
    sim.sim_param.RHO = 0.01
    sim.reset()
    sim.do_simulation()
    x = np.packet.get_interarrival_time()
    y = np.packet.get_service_time()
    plt.plot(x, y, 'o', color='black')


    pass


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    pass


if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()
