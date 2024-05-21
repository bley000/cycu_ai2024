import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
import pdfplumber

# 讀取 PDF 文件並提取測站的編號和名稱
with pdfplumber.open(r"C:\Users\User\Desktop\cycu_ai2024\TDCS使用手冊v34.pdf") as pdf:
    page = pdf.pages[0]  # 選擇需要的頁面
    text = page.extract_text()
    lines = text.split('\n')
    gantry_names = {line.split()[0]: line.split()[1] for line in lines if line.split()}

# 讀取偵測站編號與其對應經緯度的資料庫或檔案
gantry_data = pd.read_csv(r"C:\Users\User\Desktop\cycu_ai2024\gantry_data.csv")

# 將測站的名稱添加到偵測站資料庫
gantry_data['GantryName'] = gantry_data['GantryID'].map(gantry_names)

# 讀取 CSV 文件，並將時間欄位轉換為 datetime 對象
data = pd.read_csv(r"C:\Users\User\Desktop\cycu_ai2024\20240521.csv", parse_dates=['時間'])

# 將 CSV 文件與偵測站資料庫合併，以獲得每個偵測站的經緯度和名稱
data = pd.merge(data, gantry_data, how='left', left_on='GantryTo', right_on='GantryID')

# 根據行車速度創建一個新的欄位，並將其值設定為顏色代碼
data['color'] = pd.cut(data['行車速度'], bins=[0, 30, 60, float('inf')], labels=['red', 'yellow', 'green'])

# 創建一個地圖對象
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 創建一個空的 GeoJSON 物件列表
features = []

# 將每個時間點的數據添加到地圖上
for index, row in data.iterrows():
    features.append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['經度'], row['緯度']],
        },
        'properties': {
            'time': row['時間'].isoformat(),
            'style': {'color' : row['color']},
            'icon': 'circle',
            'iconstyle':{
                'fillColor': row['color'],
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': 5
            },
            'popup': '時間: ' + row['時間'].isoformat() + '<br>經度: ' + str(row['經度']) + '<br>緯度: ' + str(row['緯度']) + '<br>行車速度: ' + str(row['行車速度']) + '<br>測站名稱: ' + str(row['GantryName']),
        }
    })

# 將 GeoJSON 物件列表添加到地圖上，並創建一個時間滑塊
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT5M',
    add_last_point=True,
).add_to(m)

# 保存地圖為 HTML 文件
m.save('C:\\Users\\User\\Desktop\\traffic_map.html')