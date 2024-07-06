import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

t1 = [1,2,3,4]
l1 = [29,61.5,95.25,122.75]

t2 = []
l2 = []

def f1(x):
    return 31*x
x1 = []
y1 = []
for i in range(4):
    x1.append(i+1)
    y1.append(f1(i+1))

fig, ax = plt.subplots() #create graph

ax.plot(t1, l1,color = 'xkcd:blue') #plot real length for camera 1
ax.plot(x1,y1,color = 'xkcd:red') #plot fictional length for camera 1

ax.set(xlabel='Distance Intervals (31cm per each)',ylabel='Algorithm Output (cm)',
       title = 'Relation Between Distance and Algorithm')
ax.grid() #define x y values, title and grid

fig.savefig("graph.png")
plt.show()
