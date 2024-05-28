import os
import requests
from bs4 import BeautifulSoup
import tarfile
from datetime import datetime
import pandas as pd
import glob
import re
import shutil

# 定義網址和日期範圍
url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"
start_date = datetime.strptime('20240429', '%Y%m%d')
end_date = datetime.strptime('20240429', '%Y%m%d')

# 抓取網頁上的所有連結
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')

# 過濾出我們需要的連結
filtered_links = []
for link in links:
    name = link.get('href')
    file_name = name  # 將這行程式碼移到這裡，確保 file_name 在任何情況下都會被定義
    if name.endswith('.tar.gz'):
        date_str = name.split('_')[1].split('.')[0]
        date = datetime.strptime(date_str, '%Y%m%d')
        if start_date <= date <= end_date:
            filtered_links.append(url + name)
        # 下載這些連結的內容
        print(file_name)
        response = requests.get(url + name, stream=True)
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        # 如果下載的是壓縮檔，則解壓縮到桌面
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        tar = tarfile.open(file_name)
        tar.extractall(path=desktop_path)
        tar.close()
        os.remove(file_name)  # 刪除壓縮檔

        # 讀取並合併同一天的資料
        date_strs = [datetime.strftime(date, '%Y%m%d') for date in pd.date_range(start_date, end_date)]
        for date_str in date_strs:
            folder_path = os.path.join(desktop_path, 'M05A', date_str)
            file_paths = glob.glob(os.path.join(folder_path, '**/*.csv'), recursive=True)
            dfs = []
            for file_path in file_paths:
                df = pd.read_csv(file_path)
                dfs.append(df)

            # 使用concat函數合併所有的DataFrame
            merged_df = pd.concat(dfs)

            # 儲存合併後的DataFrame到一個新的CSV檔案，檔名為該檔案的日期
            merged_df.to_csv(os.path.join(desktop_path, 'M05A', f'{date_str}.csv'), index=False)

            # 刪除原先的資料夾
            shutil.rmtree(folder_path)
    else:
        print(file_name)
        date_str = url.rstrip('/').split('/')[5]
        from datetime import datetime
        
        date = datetime.strptime(date_str, '%Y%m%d')
        if start_date <= date <= end_date:
            filtered_links.append(url + name)
        # 對於每一天的每一個小時的每一個五分鐘，下載對應的CSV檔案
        for date_str in date_strs:
            # ...
            for hour in range(24):
                for minute in range(0, 60, 5):
                    # 建立完整的URL
                    csv_url = f'{url}{date_str}/{str(hour).zfill(2)}/TDCS_M05A_{date_str}_{str(hour).zfill(2)}{str(minute).zfill(2)}00.csv'
                    
                    # 發送HTTP請求並下載檔案
                    response = requests.get(csv_url, stream=True)
                    csv_file_name = csv_url.split('/')[-1]
                    with open(csv_file_name, 'wb') as csv_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                csv_file.write(chunk)
                    
                    # 將CSV檔案移動到桌面的指定資料夾
                    folder_path = os.path.join(desktop_path, 'M05A', date_str, str(hour).zfill(2))
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(csv_file_name, folder_path)
                    # 找到所有的CSV檔案
                    csv_files = glob.glob(os.path.join(desktop_path, 'M05A', '**', '*.csv'), recursive=True)
    
                    # 讀取並合併這些檔案
                    dfs = [pd.read_csv(file) for file in csv_files]
                    merged_df = pd.concat(dfs)
    
                    # 儲存合併後的檔案
                    merged_df.to_csv(os.path.join(desktop_path, 'M05A', f'{date_str}.csv'), index=False)
                    print(f'{date_str}.csv','合併完成！')

print('Done!')