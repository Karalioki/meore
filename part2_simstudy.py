from matplotlib import pyplot
import random
from simparam import SimParam
from simulation import Simulation
from counter import TimeIndependentCounter
from histogram import TimeIndependentHistogram

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_2_7_1():
    """
    Here, we execute tasks 2.7.1 and 2.7.2 in the same function. This makes sense, since we use only one figure with
    four subfigures to display the plots, which makes comparability easier.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


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

    # counters for mean queue length and waiting time
    counter_mean_queue_length = TimeIndependentCounter()
    hist_mean_queue_length = TimeIndependentHistogram(sim, "q")

    counter_mean_waiting_time = TimeIndependentCounter()
    hist_mean_waiting_time = TimeIndependentHistogram(sim, "w")

    # step through number of buffer spaces...
    for S in sim.sim_param.S_VALUES:
        sim.sim_param.S = S

        counter_mean_queue_length.reset()
        hist_mean_queue_length.reset()
        counter_mean_waiting_time.reset()
        hist_mean_waiting_time.reset()

        sim.sim_param.SIM_TIME = 100000
        sim.sim_param.NO_OF_RUNS = 1000

        # repeat simulation
        for run in range(sim.sim_param.NO_OF_RUNS):
            # print(run)
            sim.reset()
            sim.do_simulation()
            # add simulation result to counters and histograms (always use the mean)
            counter_mean_queue_length.count(sim.counter_collection.cnt_ql.get_mean())
            hist_mean_queue_length.count(sim.counter_collection.cnt_ql.get_mean())
            counter_mean_waiting_time.count(sim.counter_collection.cnt_wt.get_mean())
            hist_mean_waiting_time.count(sim.counter_collection.cnt_wt.get_mean())

        pyplot.subplot(221)
        pyplot.xlabel("Mean waiting time [ms] (SIM_TIME = 100.000ms)")
        pyplot.ylabel("Distribution over n")
        hist_mean_waiting_time.report()

        pyplot.subplot(222)
        pyplot.xlabel("Mean queue length (SIM_TIME = 100.000ms)")
        pyplot.ylabel("Distribution over n")
        hist_mean_queue_length.report()

        # if desired, print statistics for queue length and waiting time
        if print_queue_length:
            print('Buffer size: ' + str(sim.sim_param.S) + ', simulation time: ' + str(
                sim.sim_param.SIM_TIME) + ', Mean buffer content: ' + str(
                counter_mean_queue_length.get_mean()) + ' Variance: ' + str(counter_mean_queue_length.get_var()))

        if print_waiting_time:
            print('Buffer size: ' + str(sim.sim_param.S) + ', simulation time: ' + str(
                sim.sim_param.SIM_TIME) + ', Mean waiting time: ' + str(
                counter_mean_waiting_time.get_mean()) + ' Variance: ' + str(counter_mean_waiting_time.get_var()))

        counter_mean_queue_length.reset()
        hist_mean_queue_length.reset()
        counter_mean_waiting_time.reset()
        hist_mean_waiting_time.reset()

        sim.sim_param.SIM_TIME = 1000000
        sim.sim_param.NO_OF_RUNS = 1000

        # repeat simulation
        for run in range(sim.sim_param.NO_OF_RUNS):
            # print(run)
            sim.reset()
            sim.do_simulation()
            # add simulation result to counters and histograms (always use the mean)
            counter_mean_queue_length.count(sim.counter_collection.cnt_ql.get_mean())
            hist_mean_queue_length.count(sim.counter_collection.cnt_ql.get_mean())
            counter_mean_waiting_time.count(sim.counter_collection.cnt_wt.get_mean())
            hist_mean_waiting_time.count(sim.counter_collection.cnt_wt.get_mean())

        pyplot.subplot(223)
        pyplot.xlabel("Mean waiting time [ms] (SIM_TIME = 1.000.000ms)")
        pyplot.ylabel("Distribution over n")
        hist_mean_waiting_time.report()

        pyplot.subplot(224)
        pyplot.xlabel("Mean queue length (SIM_TIME = 1.000.000ms)")
        pyplot.ylabel("Distribution over n")
        hist_mean_queue_length.report()

        # if desired, print statistics for queue length and waiting time
        if print_queue_length:
            print('Buffer size: ' + str(sim.sim_param.S) + ', simulation time: ' + str(
                sim.sim_param.SIM_TIME) + ', Mean buffer content: ' + str(
                counter_mean_queue_length.get_mean()) + ' Variance: ' + str(counter_mean_queue_length.get_var()))

        if print_waiting_time:
            print('Buffer size: ' + str(sim.sim_param.S) + ', simulation time: ' + str(
                sim.sim_param.SIM_TIME) + ', Mean waiting time: ' + str(
                counter_mean_waiting_time.get_mean()) + ' Variance: ' + str(counter_mean_waiting_time.get_var()))

    # set axis ranges for better comparison and display accumulated plot
    pyplot.subplot(221)
    pyplot.xlim([0, 3500])
    pyplot.subplot(223)
    pyplot.xlim([0, 3500])
    pyplot.subplot(222)
    pyplot.xlim([-.5, sim.sim_param.S_MAX + .5])
    pyplot.subplot(224)
    pyplot.xlim([-.5, sim.sim_param.S_MAX + .5])
    pyplot.show()


if __name__ == '__main__':
    task_2_7_1()
