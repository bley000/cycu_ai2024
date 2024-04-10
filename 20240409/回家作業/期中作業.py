import pandas as pd

# 讀取 CSV 文件，跳過第一行，使用 'cp950' 編碼
data = pd.read_csv(r"C:\Users\WINNIE\Documents\GitHub\cycu_ai2024\20240409\地震活動彙整_638483061786957894.csv", skiprows=1, encoding='cp950')

# 將 '地震時間' 欄位轉換為 datetime 對象
data['地震時間'] = pd.to_datetime(data['地震時間'])

# 選擇在 4/3 到 4/9 之間的數據
start_date = '2024-04-03'
end_date = '2024-04-10'
mask = (data['地震時間'] >= start_date) & (data['地震時間'] <= end_date)
data = data.loc[mask]

# 輸出數據
print(data)

# ... 其他程式碼不變 ...
import folium
from folium.plugins import TimestampedGeoJson

# 創建一個地圖對象，初始位置設為台灣
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 將 '地震時間' 欄位轉換為 datetime 對象
data['地震時間'] = pd.to_datetime(data['地震時間'])

# 創建一個空的 GeoJSON 物件列表
features = []

# 將每個地震的位置添加到 GeoJSON 物件列表中
for index, row in data.iterrows():
    # 根據 '規模' 的值設定顏色和大小
    if row['規模'] < 4:
        color = 'green'
        radius = 5
    elif row['規模'] < 5:
        color = 'yellow'
        radius = 10
    elif row['規模'] < 6:
        color = 'orange'
        radius = 15
    elif row['規模'] < 7:
        color = 'red'
        radius = 20
    else:
        color = 'purple'
        radius = 25

    features.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['經度'], row['緯度']],
        },
        'properties': {
            'time': row['地震時間'].isoformat(),
            'style': {'color' : color},
            'icon': 'circle',
            'iconstyle':{
                'fillColor': color,
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': radius
            },
            'popup': '編號: ' + str(row['編號']) + '<br>地震時間: ' + row['地震時間'].isoformat() + '<br>經度: ' + str(row['經度']) + '<br>緯度: ' + str(row['緯度']) + '<br>規模: ' + str(row['規模']) + '<br>深度: ' + str(row['深度']) + '<br>位置: ' + row['位置'],
        }
    })
# 將 GeoJSON 物件列表添加到地圖上，並創建一個時間滑塊
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT1H',
    add_last_point=True,
).add_to(m)

# 保存地圖為 HTML 文件
m.save('C:\\Users\\WINNIE\\Desktop\\earthquake_map.html')

# 保存地圖為 HTML 文件 儲存到桌面
m.save('C:\\Users\\WINNIE\\Desktop\\earthquake_map.html')
print('done!')