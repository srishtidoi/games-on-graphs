import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,1,100)
rep = x*(2-x)

#plt.xlim([-0.5, 0.5])
#plt.ylim([-0.2, 1.2])
plt.grid(True)
plt.axhline(y=0, color='k')
#plt.axvline(x=0, color='k')
plt.ylabel('Repuation after increase due to cooperation')
plt.xlabel('Repuation before increase')

plt.plot(x, rep, 'r-')
plt.plot(x, x, 'k--', linewidth=0.5)
plt.show()
