'''bley000: 資料來自於 "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/" 這個網址。
資料是以 .gz (具體格式:https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/M05A_20240416.tar.gz)或 .csv (具體格式https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20240419/00/TDCS_M05A_20240419_000000.csv) 
每個小時的資料都儲存在一個獨立的資料夾中，並且每五分鐘的資料都儲存在一個獨立的 .csv 檔案中我們需要下載並解壓縮 .gz 檔案，下載 .csv 檔案，然後讀取並合併同一天的所有 .csv 檔案。我們將合併後的資料儲存為一個新的 .csv 檔案。我們需要下載 20240101~20240430 的資料。儲存到 'C:\Users\WINNIE\Desktop'
GitHub Copilot:根據您提供的資訊，我們可以寫出以下的 Python 程式碼： 
bley000: 不論是.gz還是csv檔案，我都希望他們合併後的csv可以以這六個欄位名稱
bley000: 我希望可以用UTF-8的字體來顯示。
我希望在交通量的部分(也就是第六欄位)，可以依照VehicleType(也就是第4欄位)的數字，的方式命名:
- 交通量(小客車 31) (欄位名稱 v31)- 交通量(小貨車 32) (欄位名稱 v32)- 交通量(大客車 41) (欄位名稱 v41)- 交通量(大貨車 42) (欄位名稱 v42)- 交通量(聯結車 5)  (欄位名稱 v5)並且，在SpaceMeanSpeed(也就是第五欄位)，可以只取小客車的(也就是第4欄位=31)值其餘不變
GitHub Copilot: 您可以使用 pandas 的 `pivot_table` 函數來根據 `VehicleType` 欄位的值來創建新的欄位，並將 `交通量` 欄位的值填入對應的新欄位。同時，您可以使用條件選擇來選取 `VehicleType` 為 31 的 `SpaceMeanSpeed` 值。以下是修改後的程式碼：
bley000: 可以只留下合併好的資料，刪除未合併的資料夾嗎
GitHub Copilot: 當然可以。在合併並儲存資料後，您可以使用 `shutil` 模組的 `rmtree` 函數來刪除整個資料夾。以下是修改後的程式碼：'''
import os
import requests
import tarfile
import pandas as pd
import glob
from datetime import datetime, timedelta
from io import BytesIO
import shutil

# 基本 URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"

# 桌面路徑
desktop = 'C:\\Users\\WINNIE\\Desktop'

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
            df = pd.read_csv(file_path, names=['TimeInterval', 'GantryFrom', 'GantryTo', 'VehicleType', 'SpaceMeanSpeed', '交通量'])
            dfs.append(df)

        # 使用concat函數合併所有的DataFrame
        merged_df = pd.concat(dfs)
        # 重置索引
        merged_df = merged_df.reset_index(drop=True)
        
        # 根據 VehicleType 創建新的欄位並填入交通量的值
        for vehicle_type in [31, 32, 41, 42, 5]:
            merged_df[f'v{vehicle_type}'] = merged_df.loc[merged_df['VehicleType'] == vehicle_type, '交通量']

        # 只取 VehicleType 為 31 的 SpaceMeanSpeed 值
        merged_df['SpaceMeanSpeed'] = merged_df.loc[merged_df['VehicleType'] == 31, 'SpaceMeanSpeed']

        # 儲存合併後的DataFrame到一個新的CSV檔案，檔名為該檔案的日期
        merged_df.to_csv(os.path.join(desktop, 'M05A', f'M05A_{date_str}.csv'), index=False)
        # 刪除未合併的資料夾
        shutil.rmtree(folder_path)
        current_date += timedelta(days=1)

start_date = datetime(2024, 4, 29)
end_date = datetime(2024, 4, 29)
download_files_in_range(start_date, end_date)
print("Done!")