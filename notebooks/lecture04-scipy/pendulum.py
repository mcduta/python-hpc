# Plot the numerical and exact solutions for a simple pendulum

# to inline plots in a notebook, uncomment line below
# %matplotlib inline

import numpy as np

import matplotlib.pyplot as plt
plt.plot(t, solution[:, 0], 'b', label='theta(t)')
plt.plot(t, solution[:, 1], 'g', label='omega(t)')
plt.plot(t[0::2], pendulumTheta(t[0::2],theta0,b,m,g,l), 'ro', label='exact theta(t)')
plt.plot(t[0::2], pendulumOmega(t[0::2],theta0,b,m,g,l), 'm*', label='exact omega(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
