import os
import requests
import tarfile
import pandas as pd
import glob
from datetime import datetime, timedelta
from io import BytesIO

# 基本 URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"

# 桌面路徑
desktop = r'C:\Users\WINNIE\Desktop'

def download_csv(date, hour):
    # 建立資料夾結構
    root_folder = os.path.join(desktop, 'M05A', date, str(hour).zfill(2))
    os.makedirs(root_folder, exist_ok=True)

    # 遍歷每個 CSV 檔案
    for minute in range(0, 60, 5):
        csv_url = base_url + date + "/" + str(hour).zfill(2) + "/TDCS_M05A_" + date + "_" + str(hour).zfill(2) + str(minute).zfill(2) + "00.csv"
        response = requests.get(csv_url)
        print(csv_url)

        # 檢查 HTTP 回應碼
        if response.status_code == 200:
            # 儲存 CSV 檔案
            with open(os.path.join(root_folder, "TDCS_M05A_" + date + "_" + str(hour).zfill(2) + str(minute).zfill(2) + "00.csv"), 'wb') as f:
                f.write(response.content)

def download_gz(file_url):
    # 下載檔案
    response = requests.get(file_url)
    print("Downloading", file_url)
    # 檢查 HTTP 回應碼
    if response.status_code == 200:
        # 解壓縮檔案
        tar = tarfile.open(fileobj=BytesIO(response.content))
        tar.extractall(path=desktop)
        tar.close()

def download_files_in_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        gz_file_url = f"https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_{date_str}.tar.gz"
        response = requests.head(gz_file_url)  # 使用 HEAD 方法來檢查檔案是否存在
        
        if response.status_code == 200:
            # 如果 .gz 檔案存在，則下載並解壓縮
            download_gz(gz_file_url)
        else:
            # 如果 .gz 檔案不存在，則嘗試下載 CSV 檔案
            for hour in range(24):
                download_csv(date_str, hour)
        
        # 讀取並合併同一天的資料
        folder_path = os.path.join(desktop, 'M05A', date_str)
        file_paths = glob.glob(os.path.join(folder_path, '**/*.csv'), recursive=True)
        dfs = []
        for file_path in file_paths:
            df = pd.read_csv(file_path)
            dfs.append(df)

        # 使用concat函數合併所有的DataFrame
        merged_df = pd.concat(dfs)

        # 儲存合併後的DataFrame到一個新的CSV檔案，檔名為該檔案的日期
        merged_df.to_csv(os.path.join(desktop, 'M05A', f'{date_str}.csv'), index=False)

        current_date += timedelta(days=1)

start_date = datetime(2024, 4, 30)
end_date = datetime(2024, 4, 30)
download_files_in_range(start_date, end_date)
print("Done!")