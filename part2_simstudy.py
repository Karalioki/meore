"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""

from simparam import SimParam
from simulation import Simulation
from counter import TimeIndependentCounter
from histogram import TimeIndependentHistogram
import matplotlib.pyplot as plt


def task_2_7_1():
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want).
    """
    # TODO Task 2.7.1: Your code goes here
    sim_param = SimParam()
    sim_param.SIM_TIME = 100
    sim_param.NO_OF_RUNS = 1000
    sim = Simulation(sim_param)
    do_simulation_study(sim)

def task_2_7_2():
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    # TODO Task 2.7.2: Your code goes here or in the function above
    sim_param = SimParam()
    sim_param.NO_OF_RUNS = 1000
    sim = Simulation(sim_param)
    sim.sim_param.SIM_TIME = 1000
    do_simulation_study(sim)

def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """

    # TODO Task 2.7.1: Your code goes here
    # TODO Task 2.7.2: Your code goes here
    counter_q = TimeIndependentCounter()
    hist_q = TimeIndependentHistogram(sim, "q")
    counter_w = TimeIndependentCounter()
    hist_w = TimeIndependentHistogram(sim, "w")

    def count_statistics_for_runs():
        for _ in range(sim.sim_param.NO_OF_RUNS):
            sim.reset()
            sim.do_simulation()
            counter_q.count(sim.counter_collection.cnt_ql.get_mean())
            hist_q.count(sim.counter_collection.cnt_ql.get_mean())
            counter_w.count(sim.counter_collection.cnt_wt.get_mean())
            hist_w.count(sim.counter_collection.cnt_wt.get_mean())

    for i in sim.sim_param.S_VALUES:
        sim.sim_param.S = i
        count_statistics_for_runs()
        plt.subplot(1,2,1)
        plt.xlabel('mean queue length')
        # plt.ylabel("asd")
        hist_q.report()
        plt.subplot(1,2,2)
        plt.xlabel('mean waiting length')
        plt.ylabel("asd")
        plt.xlim([0, 100])
        hist_w.report()
    plt.show()


if __name__ == '__main__':
    task_2_7_1()
    task_2_7_2()
