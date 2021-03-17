import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys

dirname = sys.argv[1]
os.chdir(dirname) # change working directory 
files = os.listdir() # get list of all files in the working directory

# n_eps = int(sys.argv[2]) # give the numebr of eps you want to plot
# files = all_files[:n_eps]

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

        x = np.array(x)

# looping over all files for y values
fc = np.empty(len(x))
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

        fc += y_temp # sum of all fcs over all the episodes
        
        # Preparing y-values for log-log plot
        r_diff = np.array(0.02112 - x)

#print('here')
fc = fc/len(files) # taking average over all episodes
print(fc)
fd = 1 - fc # fraction of defectorsl

plt.scatter(x, fc, marker='D', facecolors='none', edgecolors='g', label='Square Lattice')
plt.plot(x, fc, 'g--')
#plt.axis([0, 0.07, 0, 1])
#plt.xticks([0, 0.01, 0.02, 0.03])

#
#
#
#

os.chdir('..')
dirname = sys.argv[2]
os.chdir(dirname) # change working directory 
files = os.listdir() # get list of all files in the working directory

# n_eps = int(sys.argv[2]) # give the numebr of eps you want to plot
# files = all_files[:n_eps]

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

        x = np.array(x)

# looping over all files for y values
fc = np.empty(len(x))
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

        fc += y_temp # sum of all fcs over all the episodes
        
        # Preparing y-values for log-log plot
        r_diff = np.absolute(0.02112 - x)

#print('here')
fc = fc/len(files) # taking average over all episodes
fd = 1 - fc # fraction of defectors

plt.scatter(x, fc, marker='D', facecolors='none', edgecolors='k', label='Random Regular')
plt.plot(x, fc, 'k--')

#
#
#
#

os.chdir('..')
dirname = sys.argv[3]
os.chdir(dirname) # change working directory 
files = os.listdir() # get list of all files in the working directory

# n_eps = int(sys.argv[2]) # give the numebr of eps you want to plot
# files = all_files[:n_eps]

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

        x = np.array(x)

# looping over all files for y values
fc = np.empty(len(x))
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

        fc += y_temp # sum of all fcs over all the episodes
        
        # Preparing y-values for log-log plot
        r_diff = np.absolute(0.02112 - x)

#print('here')
fc = fc/len(files) # taking average over all episodes
fd = 1 - fc # fraction of defectors
print(fd)

plt.scatter(x, fc, marker='D', facecolors='none', edgecolors='b', label='Q = 0.03')
plt.plot(x, fc, 'b--')

plt.legend()
plt.ylabel('Fraction of population')
plt.xlabel('r')
plt.show()
