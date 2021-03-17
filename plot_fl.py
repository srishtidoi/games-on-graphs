import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys

dirname = sys.argv[1] # give the name of the directory as an argument
os.chdir(dirname) # change working directory 
files = os.listdir() # get list of all files in the working directory

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
fc = np.zeros(len(x))
fl = np.zeros(len(x))

for filename in files:
    rows = []
    cols = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        cols = next(csvreader) # column headings out of the way
        
        for row in csvreader:
            rows.append(row)
        
        # Preparing y-values for fc plot 
        y_temp = np.array([]) # value for current episode (file)
        for row in rows:
            y_temp = np.append(y_temp, float(row[2]))

        fc += y_temp # sum of all fcs over all the episodes
        
        # Preparing z-values for fl plot 
        z_temp = np.array([]) # value for current episode (file)
        for row in rows:
            z_temp = np.append(z_temp, float(row[3]))

        fl += z_temp # sum of all fls over all the episodes
        
fc = fc/len(files) # taking average over all episodes
fl = fl/len(files)
fd = 1 - fc - fl # fraction of defectors

plt.plot(x, fc, 'g--', label='cooperators')
plt.plot(x, fl, 'k--', label='loners')
plt.plot(x, fd, 'r--', label='defectors')
plt.axis([0, 0.5, 0, 1])
plt.legend()
plt.ylabel('Frequency')
plt.xlabel('r')
#plt.xticks([0, 0.01, 0.02, 0.03])
plt.show()

