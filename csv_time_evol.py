import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import re
import sys
import random as rnd


#####################################################################

n_plots = 50

#####################################################################

all_files = os.listdir() # get list of all files in the working directory
n_eps = 1

files = []
for f in all_files:
    text_file = re.search('timeseries', f)
    if text_file is not None:
        files.append(text_file.string)

#files.sort()
print(files)

def import_csv(csvfilename):
    data = []
    with open(csvfilename, "r") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        cols = next(reader)
        for row in reader:
            if row:  # avoid blank lines
                columns = [int(row[0]), float(row[1]), float(row[2]), float(row[3])]
                data.append(columns)
    return data

for n in range(n_plots):
    print(n)
    filename = files[n]
    print(filename)
    lens = []
    for ep in range(n_eps):
        data = import_csv(filename)
        length = 0
        for row in data:
            if row:
                length += 1
        lens.append(length)
        
    max_len = max(lens)
    
    fc_avg = []
    for n in range(max_len):
        fc_sum = 0
        for ep in range(n_eps):
            data = import_csv(filename)
            if n<len(data):
                fc_sum += data[n][3]
            else:
                fc_sum += data[-1][3]
            
        fc_sum = fc_sum/n_eps
        #print(fc_sum)
        fc_avg.append(fc_sum)
        
    plt.plot(range(max_len), fc_avg, 'k-', label=n, linewidth=0.5)
    #plt.xlim([0,1])
    plt.ylim([0,1])

plt.show()



