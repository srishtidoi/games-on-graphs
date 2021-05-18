import numpy as np
import matplotlib.pyplot as plt
import random as rnd

for n in range(10):
    i = 0
    rep = rnd.uniform(0,0.25)
    print(rep)
    while abs(1-rep)>0.001:
        rep = -0.9311 + 2/(1+np.exp(-rep/0.3))
        i+=1

    print(i)

root = 2.25/2.3 - 0.913

#while abs(rep+1)>0.001:
# while i<25:
#     if rep>root:
#         rep = -0.5*np.log((-1/1.3) + 2.25/(1.3*(rep+0.913)))
#     elif rep<-root:
#         rep = 0.5*np.log((-1/1.3) + 2.25/(1.3*(-rep+0.913)))
#     else:
#         if rep>0:
#             rep = -root
#         else:
#             rep = root
#     i+=1
#     print(rep)

print(i)
xp = np.linspace(0, 1, 100)
xn = np.linspace(-1, 0, 100)

yp = -0.913 + 2.25/(1+1.3*np.exp(-xp/0.5))
plt.plot(xp, yp, 'r-')
plt.plot(xp, xp, 'b--', linewidth=0.5)

yn = 0.913 - 2.25/(1+1.3*np.exp(xn/0.5))
plt.plot(xn, yn, 'r-')
plt.plot(xn, xn, 'b--', linewidth=0.5)

plt.grid(True)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

#plt.show()
