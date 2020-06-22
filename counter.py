import math
from typing import Union

import numpy
import scipy
import scipy.stats


class Counter(object):
    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print('Name: ' + str(self.name) + ', Mean: ' + str(self.get_mean()) + ', Variance: ' + str(self.get_var()))
        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):
    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """

    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)

    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        if len(self.values) > 0:
            return numpy.mean(self.values)
        else:
            return 0

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        return numpy.var(self.values, ddof=1)

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        return numpy.std(self.values, ddof=1)

    def report_confidence_interval(self, alpha=0.05, print_report=True):
        n = len(self.values)
        var = self.get_var()
        t = scipy.stats.t.ppf(1 - (alpha / 2), n - 1)
        if print_report:
            print("[confidence interval:"+str(self.get_mean()-t * (math.sqrt(var / n)))+ " "+str(self.get_mean()+t * (math.sqrt(var / n))) + "]")

        return t * (math.sqrt(var / n))
        pass

    def is_in_confidence_interval(self, x, alpha=0.05, print_report=True):
        mean = self.get_mean()
        low = mean - self.report_confidence_interval(alpha)
        upper = mean + self.report_confidence_interval(alpha)
        if low <= x <= upper:
            return True
        else:
            return False

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000):
        theta_static = self.get_mean()
        bootstrap_difference = []
        for i in range(resample_size):
            resample_data = numpy.random.choice(self.values, len(self.values))
            theta_resample = numpy.mean(resample_data)
            bootstrap_difference.append(theta_resample - theta_static)

        bootstrap_difference = numpy.sort(bootstrap_difference)
        quantile_low = numpy.quantile(bootstrap_difference, 1 - 0.5 * alpha)
        quantile_upper = numpy.quantile(bootstrap_difference, 0.5 * alpha)
        low_bound = theta_static - quantile_low
        upper_bound = theta_static - quantile_upper
        return low_bound, upper_bound

    def is_in_bootstrap_confidence_interval(self, x, alpha=0.05, resample_size=5000):
        (low, upper) = self.report_bootstrap_confidence_interval(alpha, resample_size)

        if low <= x <= upper:
            return True
        else:
            return False


class TimeDependentCounter(Counter):
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """

    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.sum_power_two = []  # second moment used for variance calculation

    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """
        dt = self.sim.sim_state.now - self.last_timestamp
        if dt < 0:
            print('Error in calculating time dependent statistics. Current time is smaller than last timestamp.')
            raise ValueError
        self.sum_power_two.append(value * value * dt)
        self.values.append(value * dt)
        self.last_timestamp = self.sim.sim_state.now

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        return float(sum(self.values)) / float((self.last_timestamp - self.first_timestamp))

    def get_var(self):
        """
        Return the variance of the TDC.
        """
        dt = self.last_timestamp - self.first_timestamp
        return float(sum(self.sum_power_two)) / float(dt) - self.get_mean() * self.get_mean()

    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        return numpy.sqrt(self.get_var())

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        self.sum_power_two = []
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):
    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        self.x = TimeIndependentCounter()
        self.y = TimeIndependentCounter()
        self.xy = TimeIndependentCounter()
        self.reset()

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        self.x.reset()
        self.y.reset()
        self.xy.reset()

    def count(self, x, y):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        self.x.count(x)
        self.y.count(y)
        self.xy.count(x * y)

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.

        Simple calculation with numpy:
        cov = numpy.cov(self.x.values, self.y.values, ddof=0)[0, 1]
        """
        return self.xy.get_mean() - self.x.get_mean() * self.y.get_mean()

    def get_cor(self):
        """
        Calculate the correlation coefficient between the two internal arrays x and y.

        Simple calculation with numpy:
        cor = numpy.corrcoef(self.x.values, self.y.values, ddof=0)[0, 1]
        """
        return self.get_cov() / math.sqrt(self.x.get_var() * self.y.get_var())

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print('Name: ' + self.name + '; covariance = ' + str(self.get_cov()) + '; correlation = ' + str(self.get_cor()))


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):
    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        self.max_lag = max_lag
        self.reset()

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.
        :return: auto covariance
        """
        if lag <= self.max_lag:
            x = self.values
            y = self.values[-lag:] + self.values[:-1 * lag]
            xy = []

            for i in range(len(x)):
                xy.append(x[i] * y[i])

            return numpy.mean(xy) - numpy.mean(x) * numpy.mean(y)

        else:
            raise RuntimeError("lag larger than max_lag, please correct!")

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation coefficient
        """
        if lag <= self.max_lag:
            var = self.get_var()
            if var != 0:
                return self.get_auto_cov(lag) / var
            else:
                return 0.0
        else:
            raise RuntimeError("lag larger than max_lag, please correct!")

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        self.max_lag = max_lag
        self.reset()

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print('Name: ' + self.name)
        for i in range(0, self.max_lag + 1):
            print('Lag = ' + str(i) + '; covariance = ' + str(self.get_auto_cov(i)) + '; correlation = ' + str(
                self.get_auto_cor(i)))
