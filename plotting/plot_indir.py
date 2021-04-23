import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import re
import sys
import random as rnd



####
# the max value of x for fitting and showing

x_max = 0.5

####


all_files = os.listdir() # get list of all files in the working directory

files = []
for f in all_files:
        text_file = re.search('csv', f)
        if text_file is not None:
                files.append(text_file.string)
        
n_eps = int(sys.argv[1]) # give the number of eps you want to plot
files = rnd.sample(files, n_eps) # pick n-eps number of eps at random

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
fit = np.poly1d(np.polyfit(x, fc, 3))
fit_x = np.linspace(0, x_max, 100)

plt.scatter(x, fc, s=3, edgecolors='g', label = 'cooperators')
plt.plot(fit_x, fit(fit_x), linewidth=1)
#plt.plot(x, fc, 'k-', alpha=0.8)

plt.ylabel('Fraction of cooperators')
plt.xlabel('r')
plt.xlim([0,x_max])
plt.ylim([0,1])
#plt.axis([0, 0.07, 0, 1])
#plt.xticks([0, 0.01, 0.02, 0.03])
#plt.legend()

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

