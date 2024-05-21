import os
import requests

# 基本 URL
base_url = "https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/"

# 指定日期
date = "20240429"

# 桌面路徑
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# 建立資料夾結構
root_folder = os.path.join(desktop, 'M05A', date)
os.makedirs(root_folder, exist_ok=True)

# 遍歷每個小時
for hour in range(24):
    hour_folder = os.path.join(root_folder, str(hour).zfill(2))
    os.makedirs(hour_folder, exist_ok=True)

    # 遍歷每個 CSV 檔案
    for minute in range(0, 60, 5):
        csv_url = base_url + date + "/" + str(hour).zfill(2) + "/TDCS_M05A_" + date + "_" + str(hour).zfill(2) + str(minute).zfill(2) + "00.csv"
        response = requests.get(csv_url)
        print(csv_url)

        # 檢查 HTTP 回應碼
        if response.status_code == 200:
            # 儲存 CSV 檔案
            with open(os.path.join(hour_folder, "TDCS_M05A_" + date + "_" + str(hour).zfill(2) + str(minute).zfill(2) + "00.csv"), 'wb') as f:
                f.write(response.content)