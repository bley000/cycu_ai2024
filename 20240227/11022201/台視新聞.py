#https://news.ltn.com.tw/rss/all.xml
import feedparser

# 1. 使用 feedparser.parse 來解析 RSS feed
feed = feedparser.parse('https://www.ttv.com.tw/rss/RSSHandler.ashx?d=news')

# 2. feed.entries 包含了所有的新聞項目或氣象報告
for entry in feed.entries:
    # 3. 每個 entry 都是一個字典，包含了 title, link, description 等欄位
    print(f"Title: {entry['title']}")
    print(f"Description: {entry['description']}")
    print("=================\n")
    if "50歲男" in entry.title:
        import csv
        with open('news.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Description'])
            writer.writerow([entry['title'], entry['description']])
            csvfile.close()
