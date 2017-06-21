
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1)
fig.set_size_inches(4.0, 8.0)

plt.suptitle("THREE PLOTS", fontsize = 20)
plt.subplots_adjust(left = 0.2)

pie_labels = 'A', 'B', 'C', 'D'
pie_sizes = [15, 30, 35, 20]
pie_colours = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
pie_radius = 1.1
pie_angle = 90

plt.sca(axes[0])
plt.axis('equal')
plt.pie(pie_sizes, labels=pie_labels, colors=pie_colours,
        autopct = '%1.0f%%', shadow = False, startangle = pie_angle,
        radius = pie_radius)

data1 = np.genfromtxt("uniform.dat")

plt.sca(axes[1])
plt.hist(data1, bins = 10, normed = 1, color = "m", label = "Uniform")
plt.ylabel("$P(x)$", size = 18)
plt.legend()

data2 = np.genfromtxt("normal.dat")

plt.sca(axes[2])
plt.hist(data2, bins = 10, normed = True, color = "g", label = "Normal")
plt.xlabel("Variable $x$", size = 18)
plt.ylabel("$P(x)$", size = 18)
plt.legend()

plt.show()
