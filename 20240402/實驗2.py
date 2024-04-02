import requests
from bs4 import BeautifulSoup
import re
import geopandas as gpd
import matplotlib.pyplot as plt

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
    print(f'{city_name}: {temperature}')

# 讀取.shp檔案
gdf = gpd.read_file('c:\\Users\\User\\Desktop\\新增資料夾 (2)\\TOWN_MOI_1120825.shp')

# 將溫度數據添加到地理數據框中
# 請將'TOWNNAME'替換為你的數據框中包含城市名稱的列名
gdf['temperature'] = gdf['COUNTYNAME'].map(city_dict)

# 繪製地圖和溫度數據
fig, ax = plt.subplots(1, 1)
# 讀取.shp檔案
gdf = gpd.read_file('c:\\Users\\User\\Desktop\\新增資料夾 (2)\\TOWN_MOI_1120825.shp')



# 檢查gdf是否為空
if gdf.empty:
    print("The geodataframe is empty. Please check the path to the .shp file.")
else:
    # 將溫度數據添加到地理數據框中
    # 請將'TOWNNAME'替換為你的數據框中包含城市名稱的列名
    gdf['temperature'] = gdf['COUNTYNAME'].map(city_dict)

    # 檢查是否所有的城市名稱都能在city_dict中找到
    if gdf['temperature'].isnull().any():
        print("Some city names in the geodataframe could not be found in the temperature data. Please check the city names.")
    else:
        # 繪製地圖和溫度數據
        fig, ax = plt.subplots(1, 1)
        gdf.plot(column='temperature', ax=ax, legend=True)

        # 顯示圖形
        plt.show()
        gdf.plot(column='temperature', ax=ax, legend=True)
# 顯示圖形
plt.show()