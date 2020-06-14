from rng import ExponentialRNS, UniformRNS
from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
import time
import numpy


def draw_hist_util():
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    sim = Simulation()
    cnt = TimeIndependentCounter("sys_util")
    sim.sim_param.S = 5
    fig = pyplot.figure(figsize=(24, 16))

    rho_index = 1
    for rho in [0.01, 0.5, 0.8, 0.9]:

        ax = fig.add_subplot(2, 2, rho_index)
        rho_index += 1
        time_index = 1
        print('___________________________')
        print('rho is %s' % rho)

        for sim_time in [100, 1000, 10000]:

            sim.sim_param.SIM_TIME = sim_time * 1000
            sim.sim_param.RHO = rho

            print('sim_time is %s' % sim_time)

            cnt.reset()
            for _ in range(100):
                sim.sim_param.SEED_IAT += 2
                sim.sim_param.SEED_ST += 2
                sim.reset()
                cnt.count(sim.do_simulation().system_utilization)

            # Create the histogram
            values = cnt.values
            weights = numpy.full(len(values), 1.0 / float(len(values)))
            histogram, bins = numpy.histogram(values, weights=weights, bins=25, range=(0, 1))

            total_width = .04 * .8
            width = total_width / float(3)

            ind = bins[0:len(bins) - 1] + .004 + (time_index - 1) * width
            ax.bar(ind, histogram, width=width, label='sim time = ' + str(sim_time) + " s",
                   color=colors[time_index - 1])
            time_index += 1

            print('Mean utilization is %s' % cnt.get_mean())
            # print('separate values')
            # print(cnt.values)

        ax.set_title("rho = %s" % rho)
        ax.legend(loc='upper left')
    pyplot.show()


def plot_queue_size_vs_throughput():
    sim = Simulation()
    cnt_u = TimeIndependentCounter("sys_util")
    cnt_b = TimeIndependentCounter("block_prob")
    sim.sim_param.RHO = 0.9
    sim.sim_param.SIM_TIME = 1000000

    sys_util = []
    block_prob = []
    queue_size_range = range(2, 21, 1)
    for queue_size in queue_size_range:
        sim.sim_param.S = queue_size
        cnt_u.reset()
        cnt_b.reset()
        for _ in range(100):
            sim.sim_param.SEED_IAT += 2
            sim.sim_param.SEED_ST += 2
            sim.reset()
            cnt_u.count(sim.do_simulation().system_utilization)
            cnt_b.count(sim.do_simulation().blocking_probability)
        sys_util.append(cnt_u.get_mean())
        block_prob.append(cnt_b.get_mean())

    fig = pyplot.figure()
    # figsize=(16, 16)
    ax = fig.add_subplot(2, 1, 1)
    ax.plot(range(len(sys_util)), sys_util)
    ax.set_xticks(range(len(sys_util)))
    ax.set_xticklabels(queue_size_range)
    ax.set_title("system throughput vs queue size")
    ax.set_xlabel("queue size")
    ax.set_ylabel("system throughput")

    ax = fig.add_subplot(2, 1, 2)
    ax.plot(range(len(block_prob)), block_prob)
    ax.set_xticks(range(len(block_prob)))
    ax.set_xticklabels(queue_size_range)
    ax.set_title("blocking probability vs queue size")
    ax.set_xlabel("queue size")
    ax.set_ylabel("blocking probability")
    pyplot.tight_layout()
    pyplot.show()


def plot_iat_distribution():
    sim = Simulation()
    sim.sim_param.RHO = 0.8

    sim.sim_param.SIM_TIME = 100000
    sim.reset()


if __name__ == "__main__":
    draw_hist_util()
    # plot_queue_size_vs_throughput()
