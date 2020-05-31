from finitequeue import FiniteQueue
from packet import Packet

class SystemState(object):
    
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the queue (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        """
        self.buffer = FiniteQueue(sim)
        self.served_packet = None
        self.last_arrival = 0
        self.buffer_content = 0
        self.server_busy = False
        self.sim = sim

    def get_queue_length(self):
        return self.buffer.get_queue_length()

    def add_packet_to_server(self):
        """
        Try to add a packet to the server unit.
        :return: True if server is not busy and packet has been added successfully.
        """
        if self.server_busy:
            return False
        else:
            if not self.buffer.is_empty():
                self.buffer.remove()
                packet = Packet(self.sim)
                packet.start_service()
                self.server_busy = True
                self.served_packet = 1
            else:
                packet = Packet(self.sim)
                packet.start_service()
                self.served_packet = 1
                self.server_busy = True
            return True

    def add_packet_to_queue(self):
        """
        Try to add a packet to the buffer.
        :return: True if buffer/queue is not full and packet has been added successfully.
        """
        if self.get_queue_length() < self.sim.sim_param.S:
            packet = Packet(self.sim)
            packet.get_waiting_time()
            self.buffer.add(packet)
            # self.buffer_content += 1
            return True
        else:
            return False
    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        self.server_busy = False

    def start_service(self):
        """
        If the buffer is not empty, take the next packet from there and serve it.
        :return: True if buffer is not empty and a stored packet is being served.
        """
        if self.buffer_content == 0:
            return False
        else:
            self.buffer_content -= 1
            self.server_busy = True
            return True
