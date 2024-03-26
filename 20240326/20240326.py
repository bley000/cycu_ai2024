import requests
import pandas as pd
from io import StringIO
import time

# 建立一個空的 DataFrame 來儲存所有的資料
all_data = pd.DataFrame()

# 從每個小時的 URL 下載 CSV 檔案
for hour in range(24):
    # 定義 URL 和檔案名稱
    url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240325/{hour:02d}/"
    file_names = [f"TDCS_M05A_20240325_{hour:02d}{i:04d}.csv" for i in range(0, 5501, 500)]
    
    # 從每個 URL 下載 CSV 檔案
    for file_name in file_names:
        response = requests.get(url + file_name)
        data = pd.read_csv(StringIO(response.text), header=None)

        # 將 DataFrame 的欄位重新命名
        data.columns = ['時間', '上游偵測站編號', '下游偵測站編號', '車種', '中位數旅行時間', '交通量']

        # 將這個檔案的資料中的換行符和回車符替換為空格
        for column in data.columns:
            data[column] = data[column].astype(str).replace('\n', ' ', regex=True).replace('\r', ' ', regex=True)

        # 將這個檔案的資料加到 all_data DataFrame 中
        all_data = pd.concat([all_data, data])

        # 在每次請求之間加入一些延遲
        time.sleep(0.3)

        # 輸出一條訊息
        print(f"已經完成檔案 {file_name}")

# 將所有的資料儲存到桌面，並指定分隔符號和編碼
all_data.to_csv("C:/Users/WINNIE/Desktop/20240325.csv", index=False, sep=',', encoding='utf-8-sig')