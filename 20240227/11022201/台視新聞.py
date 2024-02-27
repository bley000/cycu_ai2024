import requests
import feedparser

url='https://news.pts.org.tw/xml/newsfeed.xml'
response = requests.get(url)

feed = feedparser.parse(response.content)

for entry in feed.entries:
    print(entry.title)
    #印出 summary
    print(entry.summary)
    #印出區隔線
    print('=====================')
    #檢查檔案的標題是否包含 蔣萬安 如果有就儲存成 excel 可讀取的格式
    #放在 使用者的桌面上
    #檔案名稱是 news.xlsx
    if '蔣萬安' in entry.title:
        import pandas as pd
        df = pd.DataFrame([entry.title, entry.summary])
        df.to_excel('C:\\Users\\user\\Desktop\\news.xlsx', index=False)
  