import os  # 導入 os 模塊
import pandas as pd
import plotly.graph_objects as go

# 讀取 csv 檔案
df = pd.read_csv("C:\\Users\\WINNIE\\Desktop\\M05A\\M05A_20240429_feature.csv")

# 只保留 VehicleType 為 31 的數據
df = df[df['VehicleType'] == 31]

# 將時間欄位轉換為 datetime 對象
df['OriginalTimeInterval'] = pd.to_datetime(df['OriginalTimeInterval'])

# 定義顏色尺度
colorscale = [[0, 'white'], [0.2, 'purple'], [0.4, 'red'], [0.6, 'orange'], [0.8, 'yellow'], [1, 'green']]

# 創建 3D 曲線圖，使用 'SpeedClass' 作為車速的欄位
fig = go.Figure(data=go.Scatter3d(
    x=df['OriginalTimeInterval'],
    y=df['WayMilageFrom'],
    z=df['v31'],
    mode='lines',
    line=dict(
        color=df['SpeedClass'],
        colorscale=colorscale,
        width=2,
        cmin=0,
        cmax=5,
        colorbar=dict(
            title='Speed Class',
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif'
            ),
            thickness=15,
            len=0.5,
            x=1.05,
            y=0.5,
            ticks='outside',
            ticklen=3,
            showticksuffix='last',
            ticksuffix=' km/h',
            dtick=1
        )
    )
))

# 設置圖表的標題和軸標籤
fig.update_layout(
    scene=dict(
        xaxis_title='Original Time Interval',
        yaxis_title='Way Milage From',
        zaxis_title='v31'
    )
)

# 保存圖表為 HTML 檔案
fig.write_html("traffic_volume_speed.html")

print("Done!")
print("Current working directory:", os.getcwd())  # 打印當前工作目錄