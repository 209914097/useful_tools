import pandas as pd
from pandas import DataFrame,Series
import os
os.system('honey.bat')
laser_ID = input('请输入激光束ID如15').split(',')
azimuth_list = input('请输入方位角范围如0,35999').split(',')
azimuth_list =[ x for x in azimuth_list if x != '' ]
if not azimuth_list:
 azimuth_list = [0,1,2,3,4,5,35999,35998,35997,35996,35995]

file_path = '3'

file_num=len(os.listdir(file_path))
file_list = os.listdir(file_path)

for i in range(file_num):
    os.rename(os.path.join(file_path, file_list[i]),file_path+'/'+str(i)+'.csv')

# -----------------------------------------------------------华丽的分割线----------------------------------------------
# for i in range(file_num):
#     frame = DataFrame(pd.read_csv(file_path+'/'+str(i)+'.csv'))
#     frame.sort_values(by=['laser_id'] ,ascending=False).to_csv(file_path+'/'+str(i)+'.csv')

# frame = DataFrame(pd.read_csv('3/0.csv'))
#
# li =frame[ frame['laser_id'].isin([5])]
# li.to_csv(file_path+'/'+str(8)+'.csv')
# print(li)

# frame = DataFrame(pd.read_csv('3/8.csv'))
# ai = frame[ frame['azimuth'].isin([0,1,2,3,4,5,35999,35998,35997,35996,35995])]
# print(ai)
# -----------------------------------------------------------华丽的分割线----------------------------------------------
for i in range(file_num):
    frame = DataFrame(pd.read_csv(file_path+'/'+str(i)+'.csv'))
    fliter = frame.sort_values(by=['laser_id'] ,ascending=False)
    laser = frame[fliter['laser_id'].isin(laser_ID)]
    # print(laser)
    laser.to_csv(file_path+'/'+str(i)+'.csv')

for i in range(file_num):
    frame = DataFrame(pd.read_csv(file_path + '/' + str(i) + '.csv'))
    azimuth = frame[frame['azimuth'].isin(azimuth_list)]
    azimuth.to_csv(file_path+'/'+str(i)+'.csv')
    # print(azimuth)
csv_list = []
file_list = os.listdir(file_path)
for i in file_list:
    csv_list.append(pd.read_csv(file_path + '/'+i))
new_csv=pd.concat(csv_list)
# print(new_csv)
new_csv.to_csv('output.csv')

te = pd.read_csv('output.csv')
te.drop(te.columns[[0,1,2]],axis=1).to_csv('output.csv')
print('筛选完成！')
