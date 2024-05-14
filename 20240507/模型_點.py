import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# 讀取 CSV 檔案
df = pd.read_csv(r"C:\Users\WINNIE\Documents\GitHub\cycu_ai2024\20240507\merged.csv")

# 過濾出 VehicleType 為 31 的資料
df = df[df['VehicleType'] == 31]

# 過濾出 GantryFrom 前三個字是 '01F' 且結尾是 'S' 的資料
df = df[df['GantryFrom'].str.startswith('01F') & df['GantryFrom'].str.endswith('S')]

# 將 GantryFrom 的 '01F' 和 'S' 取代成空字串，並將剩下的字元轉換成數字
df['GantryFrom'] = df['GantryFrom'].str.replace('01F', '').str.replace('S', '').astype(int)

# 將時間轉換為每天的第幾個五分鐘（0~288）
df['Time'] = df['TimeInterval'].str.split(' ').str[1]  # 取出時間部分
df['Time'] = df['Time'].str.split(':').apply(lambda x: int(x[0]) * 12 + int(x[1]) // 5)
df['TimeInterval'] = df['Time']
df = df.drop(columns=['Time'])  # 刪除臨時欄位

# 將數據分為特徵和標籤
X = df[['TimeInterval', 'GantryFrom']]
y = df['交通量']

# 將數據分為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 創建並訓練模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 使用模型進行預測
y_pred = model.predict(X_test)

# 創建一個規則的網格
grid_x, grid_y = np.mgrid[min(df['TimeInterval']):max(df['TimeInterval']):100j, min(df['GantryFrom']):max(df['GantryFrom']):100j]

# 使用插值函數估計網格上的值
grid_z = griddata((X_test['TimeInterval'], X_test['GantryFrom']), y_pred, (grid_x, grid_y), method='cubic')

# 將負數設為 0
grid_z = np.maximum(grid_z, 0)

# 創建一個新的變數來存儲顏色，並初始化所有元素為 'w'
colors = np.full(grid_z.shape, 'w', dtype=str)
colors[grid_z > 80] = 'g'
colors[(grid_z > 60) & (grid_z <= 80)] = 'y'
colors[(grid_z > 40) & (grid_z <= 60)] = 'c'  # 使用 'c' 代表 cyan
colors[(grid_z > 20) & (grid_z <= 40)] = 'r'
colors[(grid_z >= 0) & (grid_z <= 20)] = 'm'  # 使用 'm' 代表紫色

import matplotlib

# 設定字體為 Microsoft YaHei，支援中文顯示
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 繪製三維點狀圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 將網格轉換為一維陣列，以便於繪製點狀圖
grid_x_1d = grid_x.ravel()
grid_y_1d = grid_y.ravel()
grid_z_1d = grid_z.ravel()
colors_1d = colors.ravel()

# 繪製點狀圖
ax.scatter(grid_x_1d, grid_y_1d, grid_z_1d, c=colors_1d)

ax.set_xlabel('TimeInterval')
ax.set_ylabel('GantryFrom')
ax.set_zlabel('交通量')
plt.show()