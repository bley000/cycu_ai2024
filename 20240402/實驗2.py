import folium

# 創建一個地圖物件
m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)

# 台灣所有縣市的地理座標
city_coordinates = {
    '基隆市': [25.1275, 121.7392],
    '台北市': [25.0324, 121.5180],
    '新北市': [25.0111, 121.4458],
    
    # 添加其他縣市的座標...
}

# 遍歷所有的網址
for i in range(1, 23):
    url = f"https://www.cwa.gov.tw/rss/forecast/36_{i:02}.xml"
    
    # 抓取RSS feed
    response = requests.get(url)
    
    # 解析RSS feed
    soup = BeautifulSoup(response.content, "xml")
    
    # 提取所需的資訊
    title = soup.find("item").title.text
    
    # 獲取縣市名稱
    city_name = title.split(' ')[0]
    
    # 如果縣市在我們的座標字典中，則添加標記
    if city_name in city_coordinates:
        folium.Marker(
            city_coordinates[city_name],  # 縣市的地理座標
            popup='<i>' + title + '</i>',  # 要顯示的資訊
        ).add_to(m)

# 保存地圖為HTML文件
m.save('map.html')