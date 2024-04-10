import geopandas as gpd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re

# 讀取台灣縣市的地理資訊
taiwan = gpd.read_file('taiwan.geojson')

# 創建一個字典來存儲各縣市的氣溫
city_temperatures = {}

# 遍歷所有的網址
for i in range(1, 23):
    url = f"https://www.cwa.gov.tw/rss/forecast/36_{i:02}.xml"
    
    # 抓取RSS feed
    response = requests.get(url)
    
    # 解析RSS feed
    soup = BeautifulSoup(response.content, "xml")
    
    # 提取所需的資訊
    title = soup.find("item").title.text
    description = soup.find("item").description.text
    
    # 從描述中提取氣溫
    match = re.search(r"溫度：(\d+)", description)
    if match:
        temperature = int(match.group(1))
    else:
        temperature = None
    
    # 獲取縣市名稱
    city_name = title.split(' ')[0]
    
    # 將縣市的氣溫存儲到字典中
    city_temperatures[city_name] = temperature

# 將氣溫資訊添加到地理資訊中
taiwan['temperature'] = taiwan['name'].map(city_temperatures)

# 繪製地圖
taiwan.plot(column='temperature', cmap='coolwarm', legend=True, figsize=(10, 10))

# 顯示地圖
plt.show()
taiwan = gpd.read_file('C:\\Users\\WINNIE\\Desktop\\新增資料夾 (4)\\鄉鎮市區界線(TWD97經緯度)1120928\\TOWN_MOI_1120825.shp)