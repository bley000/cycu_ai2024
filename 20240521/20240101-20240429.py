import requests
from bs4 import BeautifulSoup
import gzip
import pandas as pd
from datetime import datetime

# 網站 URL
url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"

# 發送 GET 請求
response = requests.get(url)

# 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 找到所有的檔案鏈接
links = soup.find_all("a")

# 日期範圍
start_date = datetime.strptime("20240101", "%Y%m%d")
end_date = datetime.strptime("20240429", "%Y%m%d")

# 遍歷所有的鏈接
for link in links:
    # 獲取檔案名稱
    filename = link.get("href")
    
    # 獲取檔案的日期
    file_date = datetime.strptime(filename.split("/")[-1].split(".")[0], "%Y%m%d")
    
    # 檢查日期是否在範圍內
    if start_date <= file_date <= end_date:
        # 獲取檔案的類型
        file_type = filename.split(".")[-1]
        
        # 根據檔案類型讀取檔案
        if file_type == "gz":
            with gzip.open(requests.get(url + filename, stream=True).raw, "rb") as f:
                content = f.read()
        elif file_type == "csv":
            content = pd.read_csv(url + filename)