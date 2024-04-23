import requests
import pandas as pd
from io import StringIO

# 創建一個空的數據框來存儲所有的數據
data = pd.DataFrame()

# 外部迴圈從 0 到 23，每次增加 1
for hour in range(24):
    # 內部迴圈從 0 到 55，每次增加 5
    for minute in range(0, 60, 5):
        # 生成新的 URL
        url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240422/{hour:02d}/TDCS_M05A_20240423_{hour:02d}{minute:02d}00.csv"
        
        # 下載 CSV 文件
        response = requests.get(url)
        
        # 確保我們得到了一個好的響應
        if response.status_code == 200:
            # 讀取 CSV 數據並添加到數據框中
            df = pd.read_csv(StringIO(response.text))
            data = pd.concat([data, df])

# 將合併的數據框保存為一個新的 CSV 文件
data.to_csv("20240423.csv", index=False)