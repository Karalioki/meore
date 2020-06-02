import numpy
from matplotlib import pyplot


class Histogram(object):

    """
    Histogram can take values for statistics and plot a histogram from them.

    Values are added to the internal array. The class is able to generate a histogram and plot it using pyplot.
    This class is an abstract class and contains some methods, that need to be implemented in subclass.
    """

    # colors for plotting multiple plots in one figure
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, sim, typestr):
        """
        Constructor for a simple histogram
        :param sim: simulation, the histogram object belongs to
        :param typestr is mainly for the sake of distinguishing between multiple histograms but information can also
        be used for configuring the plot
        """
        self.sim = sim
        self.values = []
        self.histogram = None
        self.bins = []
        self.bin_mids = []
        self.type = typestr

    def count(self, value):
        """
        Add a value to the histogram.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please implement method")

    def reset(self):
        """
        Reset all values to their initial state.
        """
        self.values = []
        self.histogram = None
        self.bins = []
        self.bin_mids = []

    def report(self):
        """
        Show the histogram to the viewer.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError

    def plot(self, diag_type="histogram", show_plot=False):
        """
        Plot function for histogram.
        :param diag_type: string can be "histogram" for a standard bar plot (default), "side-by-side" for a
        side by side histogram or "line" for a line plot
        :param show_plot: display plot after generating it. Can be set to False, if the figure contains multiple plots.
        """
        width = self.bins[1] - self.bins[0]
        self.bin_mids = [x+(width/2.) for x in self.bins[0:len(self.bins)-1]]

        if diag_type == "line":
            """
            Plot line plot - mainly thought for mean waiting time
            """
            # pyplot.plot(self.bin_mids, self.histogram, "+-", label='S=' + str(self.sim.sim_param.S))

        elif diag_type == "side-by-side":
            """
            Plot side-by-side histogram plot - mainly thought for mean queue length
            """
            # TODO Task 2.4.4: Your code goes here somewhere
            self.sim.sim_param.S_VALUES = [5, 6, 7]

            for i in range(len(self.sim.sim_param.S_VALUES)):
                if self.sim.sim_param.S_VALUES == self.sim.sim_param.S:
                    c = i
            x = self.bins[0:len(self.bins)-1]
            # x = numpy.arange(len(labels))  # the label locations
            # width = 0.35  # the width of the bars
            # if labels[] != self.sim.sim_param.S:
            #     labels.append(labels)
            pyplot.subplot(x, self.histogram, width, label='S=' + str(self.sim.sim_param.S), color=Histogram.colors[c])

        elif diag_type == "histogram":
            """
            Plot histogram - mainly thought for mean queue length
            (easier but worse interpretation than side-by-side)
            """
            weights = numpy.full(len(self.values), 1.0 / float(len(self.values)))
            pyplot.hist(self.values, self.bins, alpha=0.5, label='S='+str(self.sim.sim_param.S), rwidth=.7, weights=weights)

        else:
            raise TypeError("Undefined histogram plotting types: %s" % diag_type)

        pyplot.legend(loc='upper right')
        if show_plot:
            pyplot.show()


class TimeIndependentHistogram(Histogram):

    """
    Histogram for plotting values independent of their duration.
    """

    def __init__(self, sim, typestr):
        """
        Initialize histogram with the simulation it belongs to and a typestring for better distinction
        :param sim: simulation object, the histogram belongs to
        :param typestr: typestring for better distinction and selection of plot type
        q stands for queue length and will default to a side-by-side plot type
        bp stands for blocking probability and will default to a normal histogram plot type
        else, the plot type defaults to a line plot
        """
        super(TimeIndependentHistogram, self).__init__(sim, typestr)

    def count(self, value):
        """
        Add new value to histogram, i.e., the internal array.
        """
        self.values.append(value)
        # TODO Task 2.4.1: Your code goes here
        pass

    def report(self):
        """
        Make report, i.e., calculate histogram and bins using numpy.

        Calculation depends on type (makes results easier to read.
        "q" stands for queue length histogram resulting in a limited number of bins (only few possible values)
        "bp" stands for blocking probability histogram
        "w" stands for mean waiting time histogram
        After generating the report, the plot function is called (see this function in super class).
        """
        if len(self.values) != 0:

            if self.type == "q":
                min_q = 0
                max_q = self.sim.sim_param.S_MAX
                self.histogram, self.bins = numpy.histogram(self.values, bins=max_q+1, range=(min_q-1, max_q+1))
                self.plot(diag_type="side-by-side")
                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                pass

            elif self.type == "bp":
                self.histogram, self.bins = numpy.histogram(self.values, bins=numpy.sqrt(len(self.values)), range=(0, 1))
                self.plot(diag_type="histogram")

                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                pass

            elif self.type == "w":
                max_serving_time = 1000
                max_range = max_serving_time * self.sim.sim_param.S_MAX
                self.histogram, self.bins = numpy.histogram(self.values, bins=numpy.sqrt(len(self.values)), range=(0, max_range))
                self.plot(diag_type="line")
                # TODO Task 2.4.1: Your code goes here
                """
                Use numpy.histogram to calculate self.histogram and self.bins.
                Afterwards call the plot function using self.plot() with adequate parameters
                """
                pass

            else:
                raise TypeError("Undefined histogram types: %s" % self.type)

        else:
            raise ValueError("Can't plot histogram with no values.")


class TimeDependentHistogram(Histogram):

    """
    Histogram for plotting values considering their duration.
    """

    def __init__(self, sim, typestr):
        """
        Initialize histogram with the simulation it belongs to and a typestring for better distinction
        :param sim: simulation object, the histogram belongs to
        :param typestr: typestring for better distinction
        """
        super(TimeDependentHistogram, self).__init__(sim, typestr)
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.weights = []

    def count(self, value):
        """
        Add new value to histogram, i.e., the internal array.
        Consider the duration of this value as well.
        """
        self.values.append(value)
        self.weights.append(self.sim.sim_state.now - self.last_timestamp)
        self.last_timestamp = self.sim.sim_state.now

        # TODO Task 2.4.2: Your code goes here
        pass

    def reset(self):
        # TODO Task 2.4.2: Your code goes here
        self.weights = []
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        Histogram.reset(self)

    def report(self):
        """
        Make report, i.e., calculate histogram and bins using numpy.

        Plotting is not optimized, since not explicitly used in this assignment.
        After generating the report, the plot function is called (see this function in super class).
        """
        if len(self.values) != 0:
            self.histogram, self.bins = numpy.histogram(self.values, weights=self.weights, bins=50)
            self.plot(diag_type="histogram")
        else:
            raise ValueError("Can't plot histogram with no values.")
