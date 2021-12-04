import pandas as pd
import numpy as np
from text_detection import *

file_name = "test_df.csv"
df = pd.read_csv('./left_df.csv').to_numpy()
path = "./sac_timestamp/left/"

new_df = []
count = 0
for idx in df:
    if (idx[0] == 'f'):
        right_time = detect_time(idx[1])
        new_df.append([right_time, idx[1]])
        count += 1
    else:
        new_df.append(idx)


df = pd.DataFrame(new_df, columns=['time', 'filename'])
df.to_csv(file_name, encoding='utf-8', index=False)