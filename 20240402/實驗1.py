import requests
from bs4 import BeautifulSoup
import re
import geopandas as gpd
import matplotlib.pyplot as plt

# 讀取.shp檔案
data = gpd.read_file(r'c:\Users\User\Desktop\新增資料夾 (2)\TOWN_MOI_1120825.shp')

# 建立一個空的字典來存儲所有縣市區的資料
city_dict = {}

# 循環爬取每一個網頁
for i in range(1, 23):
    # 根據i生成網頁的URL
    url = f'https://www.cwa.gov.tw/rss/forecast/36_{i:02}.xml'
    
    # 爬取網頁
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    # 從網頁中抓取縣市區的名稱和資料
    city_name = soup.find('title').text
    city_data = soup.find('item').find('title').text

    # 從資料中提取氣溫
    temperature = re.search(r'溫度: (\d+ ~ \d+)', city_data)
    if temperature:
        temperature = temperature.group(1)
    else:
        temperature = 'No temperature data found'

    # 將縣市區的資料存儲到字典中
    city_dict[city_name] = temperature

# 查看數據框的列名
print(data.columns)

# 將氣溫數據添加到地理數據框中
# 請將'YourColumnName'替換為你的數據框中包含城市名稱的列名
data['temperature'] = data['COUNTYNAME'].map(city_dict)

print(data)
print(data['temperature'])
# 繪製地圖和氣溫數據
fig, ax = plt.subplots(1, 1)
data.plot(column='temperature', ax=ax, legend=True)

# 顯示圖形
plt.show()