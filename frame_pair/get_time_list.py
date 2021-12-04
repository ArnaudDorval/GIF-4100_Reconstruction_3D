import glob
import os

import pandas as pd

from text_detection import *

right_dir_of_images = "./sac_timestamp/right/"
left_dir_of_images = "./sac_timestamp/left/"
file_name = "left_df.csv"
#df = pd.DataFrame(columns=['time', 'filename'])

right_arr = []
for file in os.listdir(right_dir_of_images):
    right_arr.append(right_dir_of_images + file)

left_arr = []
for file in os.listdir(left_dir_of_images):
    left_arr.append(left_dir_of_images + file)

print("ok")
right_data = []
count = 0
for idx in left_arr:
    right_time = detect_time(idx)
    right_data.append([right_time, idx])
    #df2 = pd.DataFrame({"time" : right_time, "filename": idx})
    print(str(count))
    count += 1

df = pd.DataFrame(right_data, columns=['time', 'filename'])
df.to_csv(file_name, encoding='utf-8', index=False)