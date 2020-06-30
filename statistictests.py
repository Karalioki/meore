import numpy
import scipy.stats

class ChiSquare(object):

    def __init__(self, emp_x, emp_n, name="default"):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param name: name for better distinction of tests
        """
        self.name = name
        # TODO Task 6.1.1: Your code goes here
        self.emp_x = emp_x
        self.emp_n = emp_n
        pass

    def test_distribution(self, alpha, mean, var):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance of test
        :param mean: mean value of the gaussian distribution
        :param var: variance of the gaussian distribution
        """
        # TODO Task 6.1.1: Your code goes here
        Oi = self.emp_n
        Ei = []
        min_Ei = 5.0
        # n = len(self.emp_x)
        f = scipy.stats.norm(mean, var)
        # n = 100
        n = numpy.sum(Oi)
        k = len(self.emp_x)-1
        for i in range(k):
            expFrequency = 0
            pi = f.cdf(self.emp_x[i+1]) - f.cdf(self.emp_x[i])
            expFrequency = n * pi
            Ei.append(expFrequency)

        new_Ei = []
        new_Oi = []
        # Combined_Ei = 0
        # Combined_Oi = 0
        index = 0
        l = len(Oi) - index
        for j in range(len(Ei)):
            Combined_Ei = 0
            Combined_Oi = 0
            for i in range(index, l, 1):
                Combined_Ei = Combined_Ei + Ei[i]
                Combined_Oi = Combined_Oi + Oi[i]
                index = i
                if Combined_Ei >= min_Ei:
                    break
            new_Ei.append(Combined_Ei)
            new_Oi.append(Combined_Oi)
            Ei[index] = 0
            Oi[index] = 0
        new_Ei = numpy.trim_zeros(new_Ei, trim='fb')
        new_Oi = numpy.trim_zeros(new_Oi, trim='fb')
        if new_Ei[len(new_Ei) - 1] < min_Ei:
            new_Ei[len(new_Ei) - 2] += new_Ei[len(new_Ei) - 1]
            new_Ei[len(new_Ei) - 1] = 0
            new_Ei = numpy.trim_zeros(new_Ei, trim='fb')

            new_Oi[len(new_Oi) - 2] += new_Oi[len(new_Oi) - 1]
            new_Oi[len(new_Oi) - 1] = 0
            new_Oi = numpy.trim_zeros(new_Oi, trim='fb')

        chi2 = 0.0
        for i in range(len(new_Oi)):
            chi2 += ((new_Oi[i] - new_Ei[i])**2)/new_Ei[i]

        deg_freedom = len(new_Oi) - 2 - 1
        chi2_table = scipy.stats.chi2.ppf(1-alpha, deg_freedom)
        print("Mean=" + str(mean) + " Variance=" + str(var) + " Chi Square=" + str(chi2) \
        + " Table Chi Square=" + str(chi2_table))

        if chi2 > chi2_table:
            print("rejected.")
        else:
            print("Not rejected.")
        return chi2, chi2_table

        # a = [5, 2]
        # n = len(a)
        # r = 0
        # piu = []
        # b = 0
        # l = n - b
        # k = a[n - 1]
        # for j in range(n):
        #     r = 0
        #     # l = n-b
        #     for i in range(b, l, 1):
        #         r = r + a[i]
        #         b = i
        #         if r > 9:
        #             break
        #     piu.append(r)
        #     a[b] = 0
        #
        # piu = numpy.trim_zeros(piu, trim='fb')
        # print(piu)
        # if piu[len(piu) - 1] < 9:
        #     piu[len(piu) - 2] += piu[len(piu) - 1]
        #     piu[len(piu) - 1] = 0
        #     piu = numpy.trim_zeros(piu, trim='fb')
        # # else:
        # #     piu.append(k)
        # print(piu)
