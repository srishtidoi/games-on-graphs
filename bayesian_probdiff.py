import numpy as np
import matplotlib.pyplot as plt

x1 = np.linspace(-10,0,100)
x2 = np.linspace(0,10,100)
y = []

# for i in [0.1, 0.2, 0.3, 0.4]:
#     y_temp = -i + 2*i/(1 + np.exp(-x/1.5))
#     y.append(y_temp)


# plt.xlim([-10,10])
# plt.ylim([-0.5,0.5])
# plt.grid(True)
# plt.axhline(y=0, color='k')
# plt.axvline(x=0, color='k')
# plt.ylabel('Probability difference ($\Delta p$)')
# plt.xlabel('$P_{self} - P^{avg}_{nbrs}$')

# for i in range(len(y)):
#     label = round(0.1 + 0.1*i, 1)
#     plt.plot(x,y[i], label='$\Delta p_{max} = $'+str(label))
#     #plt.plot(x,0.1)

# plt.legend()
# plt.show()

for i in [1.5]: 
    y_temp = -0.2 + 0.4/(1 + np.exp(-x2/i))
    y.append(y_temp)

y0 = np.zeros(100)
y.append(y0)

plt.xlim([-5,10])
plt.ylim([-0.1,0.4])
plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.ylabel('factor')
plt.xlabel('$P_{self} - P^{avg}_{nbrs}$')
#plt.title('$\Delta Reputation$ x (1 + tendency)')

#label1 = 'value without PI'
#label2 = 'value with PI'
plt.plot(x2,y[0], 'r-') #, label=label1)
plt.plot(x1, y[1], 'r-') #, label=label2)


#plt.legend()
plt.show()
