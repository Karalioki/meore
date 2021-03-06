import queue


class FiniteQueue(object):
    """
    Class representing a finite queue representing the system buffer.

    It is a FIFO queue with finite capacity. Methods contain adding and removing packets
    as well as checking the fill status of the FIFO. Clearing the queue is done with the method flush.
    """

    def __init__(self, sim):
        """
        Initialize the finite queue
        :param sim: simulation object, the queue belongs to
        :return: FiniteQueue object
        """
        self.sim = sim
        self.buffer = queue.Queue()

    def add(self, packet):
        """
        Try to add a packet to the queue
        :param packet: packet which is supposed to be queued
        :return: true if packet has been enqueued, false if rejected
        """
        if self.buffer.qsize() < self.sim.sim_param.S:
            self.buffer.put(packet)
            return True
        else:
            return False

    def remove(self):
        """
        Return the first packet in line and remove it from the FIFO
        :return: first packet in line
        """
        if not self.buffer.empty():
            return self.buffer.get()
        else:
            return None

    def get_queue_length(self):
        """
        :return: fill status of the queue
        """
        return self.buffer.qsize()

    def is_empty(self):
        """
        :return: true if queue is empty
        """
        return self.buffer.empty()

    def flush(self):
        """
        erase all packets from the FIFO
        """
        self.buffer = queue.Queue()
