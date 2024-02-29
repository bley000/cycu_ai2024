#https://www.cwa.gov.tw/rss/forecast/36_04.xml
import requests
import xml.etree.ElementTree as ET

url = "https://www.cwa.gov.tw/rss/forecast/36_04.xml"
response = requests.get(url)
xml_data = response.content

root = ET.fromstring(xml_data)
items = root.findall("./channel/item")

for item in items:
    title = item.find("title").text
    description = item.find("description").text
    print(f"Title: {title}")
    print(f"Description: {description}")
    print()
#將明天的天氣預報抓下來 並新建一個 excel 檔案將資料放在裡面 並放在桌面上
import openpyxl
import os
import datetime

# 獲取明天的日期
today = datetime.date.today()
tomorrow = (today + datetime.timedelta(days=1)).strftime("%m/%d")


desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
wb = openpyxl.Workbook()
sheet = wb.active
sheet["A1"] = "Title"
sheet["B1"] = "Description"
row = 2

for item in items:
    description = item.find("description").text

    # 分割描述並找到包含明天日期的部分
    descriptions = description.split('\n')
    for desc in descriptions:
        if tomorrow in desc:
            desc_parts = desc.strip().split()
            first_three_parts = desc_parts[:6]
            sheet[f"A{row}"] = ' '.join(first_three_parts)
            print(' '.join(first_three_parts))
            row += 1
# 儲存工作簿到桌面
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
wb.save(os.path.join(desktop, "weather_forecast.xlsx"))
wb.close()
print("Done")