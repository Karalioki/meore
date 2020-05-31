from simparam import SimParam
from simulation import Simulation
import random

"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and the bonus task 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_1_7_1():
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_2():
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_3():
    """
    Execute bonus task 1.7.3.
    """
    pass


def do_simulation_study(sim):
    """
    This function performs the simulation study. Study runs as follows:
    simulation goal: in 80% of all runs only 10 packets dropped (see simparam.MAX_DROPPED for this value)
    If simulation goal is missed by far (< 70% or > 90%), the number of buffer spaces is raised by one
    If simulation goal is met or almost met: more runs are made with same number of buffer spaces
    to see whether it's just happened by an unfortunate choosing of random numbers (establish confidence).
    """
    go_on = True

    while go_on:
        num_successful_runs = 0
        for __ in range(sim.sim_param.NO_OF_RUNS):
            sim.reset()
            if sim.do_simulation().packets_dropped < sim.sim_param.MAX_DROPPED:
                num_successful_runs += 1

        print("S: " + str(sim.sim_param.S) + " GOOD/TOTAL: " + str(num_successful_runs) + "/"
              + str(sim.sim_param.NO_OF_RUNS) + " PERCENT: " + str(
            100 * num_successful_runs / sim.sim_param.NO_OF_RUNS) + "%")

        # close to criterion: make more runs to ensure, that the result is not only forced
        # by a fortunate or unfortunate choosing of random numbers
        if float(num_successful_runs) / float(sim.sim_param.NO_OF_RUNS) >= .7:
            # we may need to stop the simulation
            go_on = False

            for run in range(sim.sim_param.R - 1):
                # sim.sim_param.R - 1 defines, how many more runs are made if close to criterion
                num_successful_runs = 0

                for _ in range(sim.sim_param.NO_OF_RUNS):
                    sim.reset()
                    if sim.do_simulation().packets_dropped < sim.sim_param.MAX_DROPPED:
                        num_successful_runs += 1

                print("S: " + str(sim.sim_param.S) + " GOOD/TOTAL: " + str(num_successful_runs) + "/"
                      + str(sim.sim_param.NO_OF_RUNS) + " PERCENT: " + str(
                    100 * num_successful_runs / sim.sim_param.NO_OF_RUNS) + "%")

                # we need at least two out of three simulations to output more than 0.8 values in order to be confident
                if float(num_successful_runs) / float(sim.sim_param.NO_OF_RUNS) < .8:
                    go_on = True

        if go_on:
            # make buffer larger if criterion is not fulfilled sufficiently yet
            sim.sim_param.S += 1

    return sim.sim_param.S


if __name__ == '__main__':
    # task_1_7_1()
    task_1_7_2()
    # task_1_7_3()
