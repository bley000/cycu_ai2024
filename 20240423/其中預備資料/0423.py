import requests
import pandas as pd
from io import StringIO
import time
from datetime import datetime, timedelta

# 設定開始日期
start_date = datetime(2024, 4, 17)

# 從每個日期的 URL 下載 CSV 檔案
for day in range(6):# (包括起始日期)6天後的資料
    date = start_date + timedelta(days=day)
    
    # 建立一個空的 DataFrame 來儲存當天的資料
    daily_data = pd.DataFrame()

    # 從每個小時的 URL 下載 CSV 檔案
    for hour in range(24):
        # 定義 URL 和檔案名稱
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/{date.strftime('%Y%m%d')}/{hour:02d}/"
        file_names = [f"TDCS_M05A_{date.strftime('%Y%m%d')}_{hour:02d}{i:04d}.csv" for i in range(0, 5501, 500)]
        
        # 從每個 URL 下載 CSV 檔案
        for file_name in file_names:
            response = requests.get(url + file_name)
            data = pd.read_csv(StringIO(response.text), header=None)

            # 將 DataFrame 的欄位重新命名
            data.columns = ['時間', '上游偵測站編號', '下游偵測站編號', '車種', '中位數車速', '交通量']

            # 將這個檔案的資料中的換行符和回車符替換為空格
            for column in data.columns:
                data[column] = data[column].astype(str).replace('\n', ' ', regex=True).replace('\r', ' ', regex=True)

            # 將這個檔案的資料加到 daily_data DataFrame 中
            daily_data = pd.concat([daily_data, data])

            # 輸出一條訊息
            print(f"已經完成檔案 {file_name}")

    # 將當天的資料儲存到一個新的 CSV 檔案中
    daily_data.to_csv(f"C:/Users/WINNIE\Documents/GitHub/cycu_ai2024/data_{date.strftime('%Y%m%d')}.csv", index=False, sep=',', encoding='utf-8-sig')
    