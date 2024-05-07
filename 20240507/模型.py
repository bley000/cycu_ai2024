import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 讀取CSV文件
df = pd.read_csv(r'c:\Users\User\Desktop\M05.csv')

# 過濾出車種為小客車的數據
df = df[df['VehicleType'] == 31]

# 過濾出 GantryFrom 前三個字是 '01F' 且結尾是 'S' 的資料
df = df[df['GantryFrom '].str.startswith('01F') & df['GantryFrom '].str.endswith('S')]

# 將 GantryFrom 的 '01F' 和 'S' 取代成空字串，並將剩下的字元轉換成數字
df['GantryFrom '] = df['GantryFrom '].str.replace('01F', '').str.replace('S', '').astype(int)

# 將時間轉換為每天的第幾個五分鐘（0~288）
df['TimeInterval'] = pd.to_datetime(df['TimeInterval'])
df['TimeInterval'] = df['TimeInterval'].dt.hour * 12 + df['TimeInterval'].dt.minute // 5

# 根據 SpaceMeanSpeed 分成五個類別
conditions = [
    (df['SpaceMeanSpeed'] > 80),
    (df['SpaceMeanSpeed'] > 60) & (df['SpaceMeanSpeed'] <= 80),
    (df['SpaceMeanSpeed'] > 40) & (df['SpaceMeanSpeed'] <= 60),
    (df['SpaceMeanSpeed'] > 20) & (df['SpaceMeanSpeed'] <= 40),
    (df['SpaceMeanSpeed'] <= 20)
]
colors = ['green', 'yellow', 'orange', 'red', 'purple']
df['Color'] = np.select(conditions, colors, default='white')

# 創建3D圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 繪製三維散點圖
scatter = ax.scatter(df['TimeInterval'], df['GantryFrom '], df['交通量'], c=df['Color'])

ax.set_xlabel('Time')
ax.set_ylabel('GantryFrom ')
ax.set_zlabel('交通量')

plt.show()