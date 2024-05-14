import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import MinMaxScaler

# 讀取 CSV 檔案
df = pd.read_csv('c:\\Users\\User\\Desktop\\merged.csv')

# 將 'TimeInterval' 特徵正規化
scaler = MinMaxScaler()
df['TimeInterval'] = df['TimeInterval'].str.split(' ').str[1].str.split(':').str[0].astype(int)*12 + df['TimeInterval'].str.split(' ').str[1].str.split(':').str[1].astype(int)/5

# 將 'GantryFrom' 和 'GantryTo' 限制在僅 '01F', '03F' 和 '05F' 且 's' 結尾的資料，並將其轉換為數值型態
df = df[df['GantryFrom'].str.endswith('s') & df['GantryFrom'].str.slice(0, 3).isin(['01F', '03F', '05F'])]
df = df[df['GantryTo'].str.endswith('s') & df['GantryTo'].str.slice(0, 3).isin(['01F', '03F', '05F'])]
df['GantryFrom'] = df['GantryFrom'].str.slice(3, -1).astype(int)
df['GantryTo'] = df['GantryTo'].str.slice(3, -1).astype(int)

# 將 'VehicleType' 僅保留 '31' 的資料
df = df[df['VehicleType'] == '31']

# 繪製 3D 圖表
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['TimeInterval'], df['GantryFrom'], df['交通量'])
ax.set_xlabel('TimeInterval')
ax.set_ylabel('GantryFrom')
ax.set_zlabel('交通量')
plt.show()