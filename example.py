import torch
from dufuz import DiscreteEnvironment
from dufuz import tnorm
from dufuz.monitor import GrowthMonitor
from dufuz.defuzzify import cmean, wmean, mmean
from timeit import default_timer as time
import random


print('Running on device', torch.cuda.get_device_name('cuda:0'))

env = DiscreteEnvironment(tnorm=tnorm.lukasiewicz,
                          tol=0.01, breadth=1,
                          device=torch.device('cuda:0'))
env.monitors.append(GrowthMonitor())
values = list(range(8))
values = env.number(values)
values[3] = env.combine(env.combine(env.number(2.5), env.number(3.5)), env.number(4.5))

random.shuffle(values)

from matplotlib import pyplot as plt
_, axs = plt.subplots(len(values), 1, sharex="all", sharey="all")
for ax, val in zip(axs, values):
    val.plot(ax, hold=True)


def mergesort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        sub_array1 = arr[:mid]
        sub_array2 = arr[mid:]
        mergesort(sub_array1)
        mergesort(sub_array2)
        #INVALID = env.point(env.upper, 1)
        #sub_array1 = sub_array1+[INVALID]
        #sub_array2 = sub_array2+[INVALID]
        i = j = k = 0
        while k < len(arr):
            arr1 = env.getlist(sub_array1, i, None)
            #print(j)
            arr2 = env.getlist(sub_array2, j, None)
            if arr1 is None:
                comparison = 1
                arr[k] = arr2
            elif arr2 is None:
                comparison = 0
                arr[k] = arr1
            else:
                comparison = arr1 < arr2 #& ~(arr1 >= arr2)
                arr[k] = env.If(comparison, arr1, arr2)
            """print("----")
            print(mmean(arr1), mmean(arr2), mmean(arr[k]))
            print(comparison)
            print(arr1)
            print(arr2)
            print(arr[k])
            print(i, j)"""
            i = comparison + i
            j = 1-comparison + j
            k += 1


def bubblesort(values):
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            vali = values[i]
            valj = values[j]
            comparison = vali < valj
            values[i] = comparison.choice(vali, valj)
            values[j] = comparison.choose(valj, vali)


tic = time()
bubblesort(values)
print('Running time', time()-tic)
print([wmean(val) for val in values])
from matplotlib import pyplot as plt
_, axs = plt.subplots(len(values), 1, sharex="all", sharey="all")
for ax, val in zip(axs, values):
    val.plot(ax, hold=True)
plt.show()
env.monitors[0].plot()
