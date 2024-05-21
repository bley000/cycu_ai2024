import os
import requests
import tarfile
from datetime import datetime, timedelta
from io import BytesIO

# 網站 URL
url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"

# 日期範圍
start_date = datetime.strptime("20240101", "%Y%m%d")
end_date = datetime.strptime("20240429", "%Y%m%d")

# 桌面路徑
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# 遍歷日期範圍內的每一天
current_date = start_date
while current_date <= end_date:
    # 建立檔案的 URL
    file_url = url + "M05A_" + current_date.strftime("%Y%m%d") + ".tar.gz"
    
    # 下載檔案
    response = requests.get(file_url)
    print("Downloading", file_url)
    # 檢查 HTTP 回應碼
    if response.status_code == 200:
        # 解壓縮檔案
        tar = tarfile.open(fileobj=BytesIO(response.content))
        tar.extractall(path=desktop)
        tar.close()
    
    # 移動到下一天
    current_date += timedelta(days=1)
print("Done!")