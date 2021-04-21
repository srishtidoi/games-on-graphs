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
    text_file = re.search('txt', f)
    if text_file is not None:
        files.append(text_file.string)

files.sort()
print(files)

num_eps = 100

num_rows = []
for filename in files:
    print("starting ", filename)
    with open(filename, 'r') as forx:
        xreader = csv.reader(forx)

        rows = []
        for row in xreader:
            rows.append(row)
            #print(row)

        # num_rows is a list of list of numbers 
        num_rows_temp = []
        for row in rows:
            num_row = []

            if row[0][0] != 'r':
                num_row.append(int(row[0][8:]))
                num_row.append(float(row[1][3:]))
                num_row.append(int(row[2][6:]))
                num_row.append(float(row[3][4:]))

                #print(num_row)
            num_rows_temp.append(num_row)
        num_rows += num_rows_temp
        
eps = []
lens = []
r = 0.6

ep_data = [] # choosing one episode
# ep = 0
# for row in num_rows:
#     if len(row)>0:
#         if row[0] == ep and row[1] == r:
#             ep_data.append(row)
#         if row[0] > ep:
#             ep += 1
#             print(ep)
#             break
        
#     eps.append(ep_data)
#     lens.append(len(ep_data))

# print(eps[3][0:50])

for ep in range(num_eps): 
    print('episode ', ep)
    ep_data = [] # choosing one episode
    for row in num_rows:
        if len(row)>0:
            if row[0] == ep and row[1] == r:
                ep_data.append(row)
            if row[0] > ep:
                break
        
    eps.append(ep_data)
    lens.append(len(ep_data))

#print(eps[3][0:50])


# r_values = [0.3]
# lens = []
# r_eps = []
# for ep in eps:
#     for r in r_values:
#         r_ep = [] 
#         for row in ep:
#             if row[1] == r:
#                 r_ep.append(row)
#         lens.append(len(r_ep))
#         r_eps.append(r_ep)

print(lens)
max_len = max(lens)
print(max_len)
#max_len_ep = r_eps[lens.index(max_len)]
fc_avg = []

for n in range(max_len):
    fc_sum = 0
    for ep in eps:
        if n >= len(ep):
            fc_sum += ep[-1][3]
        else:
            fc_sum += ep[n][3]
            
    fc_avg.append(fc_sum/len(eps))

# plot time evolution for a particular r
x = np.arange(max_len)
y = fc_avg
            
plt.plot(x,y, label=r)
            
# plt.legend()
plt.show()
        
        
        


        
            

