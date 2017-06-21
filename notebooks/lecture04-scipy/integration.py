# Integral x = [0, pi/2] y = [0, 1] f(x,y) = ysin(x)
# numerically solve the integral using dblquad

import numpy as np
from scipy.integrate import dblquad

# order of arguments matters!
def integrand(y,x): 
    return y*np.sin(x)

# integrate f(x, y) = y * sin (x)
def integrate_this(): 
    (area,err) = dblquad(integrand, 0,np.pi/2, 
                         lambda x: 0, 
                         lambda x: 1)
    return area

integrate_this()
