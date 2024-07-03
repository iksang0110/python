from math import *
import numpy as np
from control import *
import control.matlab as ml
import matplotlib.pyplot as plt
import sympy as sp

t0, t1, dt = 0, 4, 1e-2
t = np.arange(t0, t1, dt)

sys1 = ml.tf([1], [1, 1])
sys2 = ml.tf([1], [1, 4])
sys3 = ml.tf([1], [1, 10])
sys4 = ml.tf([1, 12], [1])
sys = sys1*sys2*sys3*sys4
print('sys =', sys)

plt.figure(1)
r, k = ml.rlocus(sys, xlim = [-20, 10], ylim = [-10, 10])
index = 12
print('k =', k[index])
print('r =', r[index])
a = r[index][1].real
b = r[index][1].imag
print('Real part: ', a)
print('Imaginary part: ', b)
print('cos theta = ', -a/(a**2+b**2)**0.5)

plt.figure(2)
pzmap(sys)
plt.grid()
TF = k[index]*sys/(1+k[index]*sys)
print('CLTF =', TF)

plt.figure(3)
pzmap(TF)
plt.grid()

plt.figure(4)
y1, t = ml.step(TF, t)
plt.plot(t, y1, 'blue')
plt.grid()
plt.xlim([t0, t1])
plt.ylim([0, 1])
plt.legend(labels = ('y'))

print('Final value: ', y1[len(y1)-1])