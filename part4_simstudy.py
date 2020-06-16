from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation
from packet import Packet
import matplotlib.pyplot as plt


"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    autocor = TimeIndependentAutocorrelationCounter(max_lag=5)
    for i in range(5000):
        autocor.count(1)
        autocor.count(-1)
    autocor.report()

    autocor.reset()
    for i in range(5000):
        autocor.count(1)
        autocor.count(1)
        autocor.count(-1)
    autocor.report()


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000
    rho = [0.01, 0.5, 0.8, 0.95]
    for i in rho:
        sim.sim_param.RHO = i
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.report()
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
    # plt.subplots_adjust(hspace=0.6)
    plt.figure(figsize=(12, 30))

    plot_counter = 1
    for i in range(len(rho)):
        sim.reset()
        iat_st = sim.counter_collection.cnt_iat_st
        st_syst = sim.counter_collection.cnt_st_syst
        sim.sim_param.RHO = rho[i]
        sim.do_simulation()
        plt.subplot(4,2,plot_counter)
        plot_counter += 1
        plt.scatter(iat_st.X.values, iat_st.Y.values)
        plt.title("IAT VS Service Time RHO ="+ str(rho[i]))
        plt.subplot(4, 2, plot_counter)
        plot_counter +=1
        plt.scatter(st_syst.X.values, st_syst.Y.values)
        plt.title("Serving Time VS Syst Time RHO =" + str(rho[i]))

    plt.show()


    pass


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    rho = [0.01, 0.5, 0.8, 0.95]
    plt.figure(figsize=(8, 15))
    for i in rho:
        sim.reset()
        sim.sim_param.RHO = i
        sim.do_simulation_n_limit(10000)
        correlations = []
        lags = range(1, 21)
        # print(i)
        for lag in lags:
            correlations.append(sim.counter_collection.acnt_wt.get_auto_cor(lag))
        # print(correlations)
        plt.subplot(2, 1, 1)
        plt.plot(lags, correlations, '-o', label=str(i))

    plt.legend(loc='upper right')
    plt.legend(rho)

    for i in rho:
        sim.reset()
        sim.sim_param.RHO = i
        sim.do_simulation_n_limit(10000)
        correlations = []
        lags = range(1, 21)
        for lag in lags:
            correlations.append(sim.counter_collection.acnt_wt.get_auto_cor(lag))
        plt.subplot(2, 1, 2)
        plt.plot(lags, correlations, '-o', label=str(i))
    plt.legend(loc="upper right")
    plt.show()
    pass


if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()
