import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10,10,100)
y = []

for i in [0.1, 0.2, 0.3, 0.4]:
    y_temp = -i + 2*i/(1 + np.exp(-x/1.5))
    y.append(y_temp)


plt.xlim([-10,10])
plt.ylim([-0.5,0.5])
plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.ylabel('Probability difference ($\Delta p$)')
plt.xlabel('$P_{self} - P^{avg}_{nbrs}$')

for i in range(len(y)):
    label = round(0.1 + 0.1*i, 1)
    plt.plot(x,y[i], label='$\Delta p_{max} = $'+str(label))
    #plt.plot(x,0.1)

plt.legend()
plt.show()
