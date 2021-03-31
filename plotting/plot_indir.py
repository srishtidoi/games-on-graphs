import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
import random as rnd

all_files = os.listdir() # get list of all files in the working directory
#print(all_files)
all_files.remove('outputs')

n_eps = int(sys.argv[1]) # give the number of eps you want to plot
files = rnd.sample(all_files, n_eps) # pick n-eps number of eps at random

# preparing x-values (values of r)
x = []
with open('phase_diagram0.csv', 'r') as forx:
        xreader = csv.reader(forx)
        cols = next(xreader) # column headings out of the way
        
        rows = []
        for row in xreader:
            rows.append(row)
            
        for row in rows:
            x.append(float(row[1]))
            #print(row[1])
        
        x = np.array(x)
        # Preparing x-values for log-log plot
        r_diff = np.array(0.02112 - x)
        

# looping over all files for y values
fc = np.zeros(len(x))
for filename in files:
    rows = []
    cols = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        cols = next(csvreader) # column headings out of the way
        
        for row in csvreader:
            rows.append(row)
        
        # Preparing y-values for fc plot 
        y_temp = np.empty(0) # value for current episode (file)
        for row in rows:
            y_temp = np.append(y_temp, float(row[2]))

        #print('y_temp = ', y_temp)
        fc += y_temp # sum of all fcs over all the episodes
        #print('fc = ',fc)
        

print('fc = ', fc)
fc = fc/len(files) # taking average over all episodes
fd = 1 - fc # fraction of defectors

plt.scatter(x, fc, s=10, marker='D', facecolors='none', edgecolors='g', label = 'cooperators')
plt.scatter(x, fd, s=10, marker='^', facecolors='none', edgecolors='r', label = 'defectors')
#plt.plot(x, fc, 'g--')
#plt.plot(x, fd, 'r--')
plt.ylabel('Fraction of population')
plt.xlabel('r')
#plt.axis([0, 0.07, 0, 1])
#plt.xticks([0, 0.01, 0.02, 0.03])
plt.legend()

if sys.argv[2] == 'show':
        plt.show()
elif sys.argv[2] == 'save':
        plt.savefig("outputs/graf.png")


# m, b = np.polyfit(r_diff, fc, 1)

# plt.loglog(r_diff, fc, marker='D', linewidth='0')
# plt.ylabel('Fraction of population')
# ###plt.loglog(r_diff, m*r_diff+b)
# plt.axis([0, 0.1, 0, 1])
# plt.show()

