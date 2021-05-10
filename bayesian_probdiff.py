import numpy as np
import matplotlib.pyplot as plt

x1 = np.linspace(-10,10,1000)
x2 = np.linspace(0,10,100)


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

y = 1/(1 + np.exp(-x1/0.25))


plt.xlim([-1,1])
plt.ylim([-0.1,1.1])
plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.ylabel('Transition Probability')
plt.xlabel('$Reputation_{self}$')
#plt.title('$\Delta Reputation$ x (1 + tendency)')

#label1 = 'value without PI'
#label2 = 'value with PI'
#plt.plot(x2,y[0], 'r-') #, label=label1)
plt.plot(x1, y, 'r-') #, label=label2)


#plt.legend()
plt.show()
