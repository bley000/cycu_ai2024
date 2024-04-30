import pandas as pd
import requests
from io import StringIO

# 基礎URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240429/"

# 所有可能的小時
hours = [str(i).zfill(2) for i in range(24)]

# 初始化一個空的DataFrame來儲存所有的資料
all_data = pd.DataFrame()


# 遍歷所有可能的小時
for hour in hours:
    # 在每個小時的開始時重置分鐘
    minutes = [str(i*5).zfill(2) for i in range(12)]  # 每五分鐘一個檔案
    
    for minute in minutes:
        # 生成完整的URL
        url = base_url + hour + "/TDCS_M05A_20240429_" + hour + minute + "00.csv"
        print(url)
        # 下載CSV檔案
        response = requests.get(url)
        
        # 讀取CSV檔案到一個DataFrame中
        data = pd.read_csv(StringIO(response.text), header=None)
        
        # 將DataFrame的欄位重新命名
        data.columns = ['時間', '上游偵測站編號 ', '下游偵測站編號', '車種', '中位數車速','交通量']
        
        # 將這個檔案的資料加到all_data DataFrame中
        all_data = pd.concat([all_data, data])

# 將所有的資料儲存到桌面
all_data.to_csv("C:/Users/User/Desktop/M05.csv", index=False, sep=',', encoding='utf-8-sig')