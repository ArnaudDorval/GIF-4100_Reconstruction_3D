import pandas as pd
import numpy as np
from datetime import datetime, timedelta

file_name = './botte_1/pair_image.csv'
df_right = pd.read_csv ('./botte_1/right_image.csv').to_numpy()
df_left = (pd.read_csv ('./botte_1/left_image.csv')).to_numpy()

pair_list = []
smallest_diff = timedelta(hours=3, minutes=3, seconds=3)
count = 0

l_image = ""
for right in df_right:
    count += 1
    if (right[0] == 'f'):
        print("image : " + right[1] + " failed")
    else:
        rtime = datetime.strptime(right[0], '%H:%M:%S.%f')

        for left in df_left:
            if (left[0] == 'f'):
                print("image : " + left[1] + " failed")
            else:
                ltime = datetime.strptime(left[0], '%H:%M:%S.%f')
                tmp_diff = 0
                if (ltime < rtime):
                    tmp_diff = rtime - ltime
                else:
                    tmp_diff = ltime - rtime

                if (tmp_diff < smallest_diff):
                    smallest_diff = tmp_diff
                    l_image = left[1]

                #if (tmp_diff > timedelta(microseconds=35000)):
                    #break

        t = [smallest_diff, l_image, right[0]]
        print("l image : " + str(l_image))
        print("right[0]: " + str(right[0]))
        print("right[1]: " + str(right[1]))
        pair_list.append([smallest_diff, l_image, right[1]])
        smallest_diff = timedelta(hours=3, minutes=3, seconds=3)


df = pd.DataFrame(pair_list, columns=['time_delta', 'left', 'right'])
df.to_csv(file_name, encoding='utf-8', index=False)