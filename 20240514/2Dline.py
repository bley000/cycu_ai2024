import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

# 讀取 CSV 檔案
dataframe1 = pd.read_csv('c:\\Users\\User\\Desktop\\cycu_ai2024\\20240507\\M05.csv')

# 將時間轉換為數字
dataframe1['TimeInterval'] = pd.to_datetime(dataframe1['TimeInterval']).astype('int64') / 10**9

# 篩選 'GantryFrom' 列，只保留開頭為 '01F' 並且結尾為 'S' 的數據
dataframe1 = dataframe1[dataframe1['GantryFrom'].str.startswith('01F') & dataframe1['GantryFrom'].str.endswith('S')]

# 將 'GantryFrom' 列中的非數字字符移除，並將其轉換為數字
dataframe1['GantryFrom'] = dataframe1['GantryFrom'].str.extract('(\d+)').astype(int)

# 將 DataFrame 中的時間、偵測站編號和車流量數據轉換為 NumPy 數組
time = dataframe1['TimeInterval'].values
gantry = dataframe1['GantryFrom'].values
traffic = dataframe1['交通量'].values

# 創建一個新的 matplotlib 圖形，並添加兩個 3D 子圖
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax1 = fig.add_subplot(122, projection='3d')

# 對時間和偵測站編號數據進行網格化
time_grid, gantry_grid = np.meshgrid(np.linspace(time.min(), time.max(), 100), np.linspace(gantry.min(), gantry.max(), 100))

# 使用立方插值方法來計算每個網格點的車流量
from scipy.interpolate import griddata
from scipy.spatial.qhull import QhullError

try:
    traffic_grid = griddata((time, gantry), traffic, (time_grid, gantry_grid), method='cubic')
except QhullError:
    traffic_grid = griddata((time, gantry), traffic, (time_grid, gantry_grid), method='cubic', options={'QJ': ''})
# 在兩個子圖上繪製 3D 曲面圖
surf = ax.plot_surface(time_grid, gantry_grid, traffic_grid, cmap='viridis')
surf1 = ax1.plot_surface(time_grid, gantry_grid, traffic_grid, cmap='viridis')

# 設置坐標軸標籤
ax.set_xlabel('Time')
ax.set_ylabel('Gantry')
ax.set_zlabel('Traffic')

ax1.set_xlabel('Time')
ax1.set_ylabel('Gantry')
ax1.set_zlabel('Traffic')

# 調整第二個子圖的視角
ax1.view_init(elev=45, azim=60)

# 調整子圖之間的間距
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)

# 添加標題並保存圖形
ax.set_title('11022201 張家瑋')
plt.savefig('cubicspline_2v.png')

# 顯示圖形
plt.show()