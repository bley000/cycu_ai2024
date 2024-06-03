import pandas as pd
import plotly.express as px
import plotly.io as pio

# 讀取原始數據集
df = pd.read_csv("C:\\Users\\WINNIE\\Desktop\\M05A\\M05A_20240429_feature.csv")

# 讀取測站代碼與經緯度的 CSV 文件
stations = pd.read_csv("https://www.freeway.gov.tw/Upload/DownloadFiles/%E5%9C%8B%E9%81%93%E8%A8%88%E8%B2%BB%E9%96%80%E6%9E%B6%E5%BA%A7%E6%A8%99%E5%8F%8A%E9%87%8C%E7%A8%8B%E7%89%8C%E5%83%B9%E8%A1%A81110413.csv")

# 將測站代碼列的名稱改為與原始數據集中相同的名稱
stations.rename(columns={'設定收費區代碼': 'GantryFrom'}, inplace=True)

# 將測站代碼列的數據類型改為與原始數據集中相同的類型
stations['GantryFrom'] = stations['GantryFrom'].astype(df['GantryFrom'].dtype)

# 將測站的經緯度數據合併到原始數據集中
df = pd.merge(df, stations, on='GantryFrom', how='left')

# 只保留 'v31' 列中不是 NaN 的行
df = df.dropna(subset=['v31'])

# 將 'SpeedClass' 列的值從數字轉換為整數，然後再轉換為字符串
df['SpeedClass'] = df['SpeedClass'].astype(int).astype(str)

# 將數據按照 'SpeedClass' 列的值進行排序
df = df.sort_values('SpeedClass')

# 創建地理散點圖
fig = px.scatter_geo(df,
                     lat='緯度',  # 緯度列
                     lon='經度',  # 經度列
                     color='SpeedClass',  # 顏色代表速度
                     size='v31',  # 大小代表交通量
                     animation_frame='OriginalTimeInterval',  # 動畫幀代表時間
                     projection='natural earth',  # 投影方式
                     color_discrete_map={  # 設置每個 'SpeedClass' 值的顏色
                         '0': 'white',
                         '1': 'purple',
                         '2': 'red',
                         '3': 'orange',
                         '4': 'yellow',
                         '5': 'green'
                     })

# 設置地圖的範圍為台灣
fig.update_geos(
    lonaxis_range=[119, 124],  # 台灣的經度範圍
    lataxis_range=[20.5, 25.5]  # 台灣的緯度範圍
)

# 顯示圖形
fig.show()
# 將圖形保存為 HTML 文件
pio.write_html(fig, r'C:\Users\WINNIE\Documents\GitHub\cycu_ai2024\20240528\11022201_3.html')