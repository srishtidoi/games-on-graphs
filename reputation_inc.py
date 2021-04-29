import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,1,100)
#rep1 = x*((2-x)**0.1)
rep2 = x*((2-x)**0.2)

#plt.xlim([-0.5, 0.5])
#plt.ylim([-0.2, 1.2])
plt.grid(True)
plt.axhline(y=0, color='k')
#plt.axvline(x=0, color='k')
label2=('factor = 0.2')
label=('factor $\leq 0$')

plt.xlabel('P(C) before update')
plt.ylabel('P(C) after update')
#plt.plot(x, rep1, 'b-', label=label1)
plt.plot(x, rep2, 'b-', label=label2)
plt.plot(x, x, 'k--', linewidth=0.5, label=label)
plt.legend()
plt.show()
