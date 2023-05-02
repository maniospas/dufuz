from timeit import default_timer as time


class GrowthMonitor:
    def __init__(self, memory=1000):
        self.output = list()
        self.time = list()
        self.memory = memory

    def notify(self, output, _):
        self.output.append(output)
        self.time.append(time())
        if len(self.output) > self.memory:
            self.output.pop(0)
            self.time.pop(0)

    def plot(self):
        from matplotlib import pyplot as plt
        import numpy as np
        plt.plot(np.array(self.time)-self.time[0], self.output)
        plt.xlabel("sec")
        plt.ylabel("fuzzy set size")
        plt.show()
