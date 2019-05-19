'''
Run this script to generate mock data sets valid for testing
script creates 10000 samples over 2 csv files: train and test.
Use these data sets to first train the model and then test
model output should be around .5, due to randomised data
'''

import pandas as pd
import random

avg_mstry_max = 151956
avg_mstry_min = -1002027

avg_ws_min = -2
avg_ws_max = 2

avg_wr_min = -20.740741
avg_wr_max = 21.5686275

avg_onrle_max = 3
avg_onrle_min = -3

dftrain = pd.DataFrame()
for i in range(10000):
    c1 = round(random.uniform(avg_wr_min, avg_wr_max), 2)
    c2 = round(random.uniform(avg_ws_min, avg_ws_max), 2)
    c3 = random.randint(avg_mstry_min, avg_mstry_max)
    c4 = random.randint(avg_onrle_min, avg_onrle_max)
    c5 = random.randint(0,1)
    data = {'avg_wr':[c1],
            'avg_ws':[c2],
            'avg_mstry':[c3],
            'avg_onrle':[c4],
            'result':[c5]}
    df1 = pd.DataFrame(data)
    dftrain = dftrain.append(df1, ignore_index=True)
dftrain.to_csv('mock_train.csv')

