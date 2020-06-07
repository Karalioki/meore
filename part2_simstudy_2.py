import matplotlib.pyplot as plt
import random
from simparam import SimParam
from simulation import Simulation
from counter import TimeIndependentCounter
from histogram import TimeIndependentHistogram
import numpy as np


def study_waiting_time_dist():

    sim_param = SimParam()
    random.seed(0)
    sim = Simulation(sim_param)

    sim.sim_param.S = 5
    sim.sim_param.SIM_TIME = 100000  # 100 seconds

    sim.reset()
    sim.do_simulation()
    # sim.counter_collection.hist_wt.report()
    print(sim.counter_collection.cnt_wt.get_mean())
    plt.plot(sim.counter_collection.cnt_wt.values)
    plt.show()


def study_waiting_time():
    sim_param = SimParam()
    sim = Simulation(sim_param)
    sim.sim_param.S = 5
    sim.sim_param.SIM_TIME = 100000  # 100 seconds

    num_run = 100
    dataset = []
    for run in range(num_run):
        sim.reset()
        random.seed()
        sim.do_simulation()

        # Take the values (waiting time) of the first 150 packets
        dataset.append(sim.counter_collection.cnt_wt.values[0:150])

    # Manipulate the data set
    pkt_mean = []
    for pkt in range(150):
        s = 0
        for run in range(num_run):
            s += dataset[run][pkt]
        pkt_mean.append(s/float(num_run))

    plt.subplot(121)
    plt.plot(pkt_mean)
    plt.title("100s Run")
    plt.xlabel("Packet Number")
    plt.ylabel("Waiting Time (ms)")

    sim.sim_param.SIM_TIME = 1000000
    dataset = []
    for run in range(num_run):
        sim.reset()
        random.seed()
        sim.do_simulation()

        # Take the values (waiting time) of the first 1900 packets
        dataset.append(sim.counter_collection.cnt_wt.values[0:1800])

    # Manipulate the dataset
    pkt_mean = []
    for pkt in range(1800):
        s = 0
        for run in range(num_run):
            s += dataset[run][pkt]
        pkt_mean.append(s / float(num_run))

    plt.subplot(122)
    plt.plot(pkt_mean)
    plt.title("1000s Run")
    plt.xlabel("Packet Number")
    plt.ylabel("Waiting Time (ms)")


if __name__ == "__main__":
    # study_waiting_time_dist()
    study_waiting_time()
