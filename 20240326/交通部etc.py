import requests
from bs4 import BeautifulSoup
import pandas as pd

# 初始化一個空的DataFrame來存儲所有的資料
all_data = pd.DataFrame()

# 遍歷每個小時
for appale in range(5):
    # 獲取網頁的HTML內容
    url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240325/{str(appale).zfill(2)}/"
    print (url) 
    response = requests.get(url)

    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有的CSV檔案連結
    links = [url + link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.csv')]

    # 讀取並合併所有的CSV檔案
    dataframes = [pd.read_csv(link) for link in links]
    combined_df = pd.concat(dataframes)

    # 將這個小時的資料添加到所有的資料中
    all_data = pd.concat([all_data, combined_df])

# 儲存所有的資料
all_data.to_csv('output.csv', index=False)
print('Done!')