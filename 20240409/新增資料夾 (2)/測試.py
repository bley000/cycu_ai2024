import folium
import folium.plugins as plugins
import json
import pandas as pd

# 讀取 csv 檔案，將第二行視為欄位名稱
df = pd.read_csv('c:\\Users\\User\\Desktop\\地震活動彙整_638482841314992537.csv', encoding='cp950', header=1)

# 將 '地震時間' 欄位轉換為 datetime 格式
df['地震時間'] = pd.to_datetime(df['地震時間'])

# 選取 2024 年 4 月 3 日之後的所有數據
df = df.loc[df['地震時間'].dt.date >= pd.to_datetime('2024-04-03').date()]

print(df)

# 創建一個地圖對象，設定初始位置和縮放級別
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 將數據轉換為 GeoJSON 格式
data = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['經度'], row['緯度']],
            },
            'properties': {
                'time': row['地震時間'].isoformat(),
                'style': {'color' : 'red'},
                'icon': 'circle',
                'iconstyle':{
                    'fillColor': 'red',
                    'fillOpacity': 0.6,
                    'stroke': 'false',
                    'radius': 5
                },
                'popup': f"地震時間: {row['地震時間']}, 經度: {row['經度']}, 緯度: {row['緯度']}, 規模: {row['規模']}, 深度: {row['深度']}, 位置: {row['位置']}",
            }
        } for index, row in df.iterrows()
    ]
}

# 添加 TimestampedGeoJson 插件
plugins.TimestampedGeoJson(
    data,
    period='P1D',
    add_last_point=True,
).add_to(m)

# 保存地圖為 HTML 文件 將檔案存在桌面
m.save('c:\\Users\\User\\Desktop\\earthquake_map.html')