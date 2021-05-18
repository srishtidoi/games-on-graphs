import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import csv

all_files = os.listdir()

# create a list of all text files with the print outputs
files = []
for f in all_files:
    text_file = re.search('reputation', f)
    if text_file is not None:
        files.append(text_file.string)

files.sort()
print(files)


# preparing x values and finding max len
max_x = []
lens = []
for f in files:
    dataframe = pd.read_pickle(f)
    x = np.array(dataframe['timestep'])
    x_len = len(x)
    lens.append(x_len)
    max_x.append(x)

max_len = max(lens)
max_len_ind = lens.index(max_len)
max_x = np.array(max_x[max_len_ind])


# preparing y values
y_sum = []
for f in files:
    ind = files.index(f)
    dataframe = pd.read_pickle(f)
    
    for i in range(len(dataframe['reputation'].values[0])):
        y_list = [x[i] for x in dataframe['reputation'].values]
        y_len = len(y_list)
        
        for n in range(max_len - y_len):
            y_list.append(y_list[-1])

        y = np.array(y_list)
        
        
        if ind == 0:
            y_sum.append(y)
        else:
            y_sum[i] += y


for i in range(len(y_sum)):
    y_sum[i] = y_sum[i]/len(files)
    plt.plot(max_x, y_sum[i], 'k-', linewidth=0.5, alpha=0.6)

plt.xlabel('Time')
plt.ylabel('Reputation')
plt.title('Network: Scalefree')
plt.xscale('log')
plt.show()
