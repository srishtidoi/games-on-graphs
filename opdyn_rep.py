import numpy as np
import matplotlib.pyplot as plt
import random as rnd

xp = np.linspace(0, 20, 500)
xn = np.linspace(-20, 0, 1000)

yp = 1/(1 + np.exp((0.5-xp)/0.1))
yn = 0.9/(1 + np.exp(xn+5))
    

plt.figure(figsize=(10,5))
plt.plot(xp, yp, 'r-')
plt.plot(xn, yn, 'b-')
plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.ylim([-0.1, 1.7])
plt.ylabel('Transition Probability')
plt.xlabel('x')
plt.show()
