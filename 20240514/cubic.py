import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 欄位名稱
columns = ['TimeInterval', 'GantryID', 'Direction', 'VehicleType', '交通量']

# 讀取CSV檔案，並指定欄位名稱
df = pd.read_csv('c:\\Users\\User\\Desktop\\TDCS_M03A_20240429_180000.csv', names=columns)

# 篩選出VehicleType為31的資料
df = df[df['VehicleType'] == 31]

# 篩選出'GantryID'前兩個字是01F且S結尾的資料，並將01F和S都去除
df['GantryID'] = df['GantryID'].str[3:-1].astype(int)

# 讀取另一個CSV檔案
df_speed = pd.read_csv('c:\\Users\\User\\Desktop\\TDCS_M05A_20240429_180000.csv')

# 篩選出VehicleType為31的資料
df_speed = df_speed[df_speed['VehicleType'] == 31]

# 篩選出'GantryFrom'前兩個字是01F且S結尾的資料，並將01F和S都去除
df_speed['GantryFrom'] = df_speed['GantryFrom'].str[3:-1].astype(int)

# 取出'SpaceMeanSpeed'欄位的資料
speed = df_speed['SpaceMeanSpeed']

# 繪製3D曲線面圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(df['GantryID'], df['交通量'], speed)

ax.set_xlabel('GantryID')
ax.set_ylabel('交通量')
ax.set_zlabel('SpaceMeanSpeed')

plt.show()