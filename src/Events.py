
import abc
#import simulator
simulator = None

class _Event:
    """
    Abstract representation of a simulation event, which is scheduled and executed by the simulator
    """

    def __init__(self, t):
        self.schedule_time = t  #simulation time to schedule the event

    def __lt__(self, event):
        print("DEBUG: comparing")
        return self.schedule_time < event.schedule_time

    @abc.abstractmethod
    def execute(*args, **kwargs):
        pass



class WaitingEvent(_Event):
    """
    Implements the waiting phase of a vehicle when it receives a message
    """
    def __init__(self, vehicle, t):
        super().__init__(t)
        self.vehicle = vehicle
    
    def execute():
        vehicle.broadMsg()


class BroadcastEvent(_Event):
    """
    Implements a (constant) time delay from a message send to its reception by the receiver
    """
    TX_DELAY = 2    # transmission delay, expressed in ms

    def __init__(self, vehicle):
        sched_time = (1000 * TX_DELAY) / simulator.TIME_RESOLUTION
        super().__init__(sched_time)
        self.vehicle = vehicle

    def execute():
        pass
        # TODO



    


