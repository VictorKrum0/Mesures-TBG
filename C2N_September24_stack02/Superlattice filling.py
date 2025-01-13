from scipy import constants as cst
from numpy import sqrt

k = 3.4
d = 15e-9

alpha = k*cst.epsilon_0/(d*cst.e)

print(alpha)

theta = 0.2 * 2*cst.pi/360
a = 0.246e-9
ns = 8*theta**2/(sqrt(3)*a**2)
Vs = ns/alpha

print(Vs*1e3)