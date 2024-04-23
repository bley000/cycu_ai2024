import pandas as pd
import requests
from pdfminer.high_level import extract_text

# 下載 PDF 檔案
response = requests.get("https://tisvcloud.freeway.gov.tw/documents/TDCS%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8Av34.pdf")
with open('road_names.pdf', 'wb') as f:
    f.write(response.content)

# 讀取 PDF 檔案並提取文字
text = extract_text('road_names.pdf')

# 將文字轉換為一個字典，其中鍵是編號，值是道路名稱
# 這裡我們假設文字是一個表格，並且道路名稱和編號是表格的兩個欄位
road_names = {}
for line in text.split('\n'):
    parts = line.split()
    if len(parts) == 2:
        road_names[parts[0]] = parts[1]

# 讀取 CSV 檔案
data = pd.read_csv("C:/Users/WINNIE/Documents/GitHub/cycu_ai2024/20240423/其中預備資料/data_20240422.csv")

# 將編號替換為對應的道路名稱
data['上游偵測站編號'] = data['上游偵測站編號'].map(road_names)
data['下游偵測站編號'] = data['下游偵測站編號'].map(road_names)

# 根據 '中位數車速' 的值添加一個新的欄位
data['交通狀況'] = data['中位數車速'].apply(lambda x: '車多' if x < 70 else '順暢')

# 顯示結果
print(data)