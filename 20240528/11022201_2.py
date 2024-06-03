import pandas as pd
import numpy as np
import glob
import os

# 定義門架方向的轉換字典
direction_dict = {'N': '北', 'S': '南', 'W': '西', 'E': '東'}

# 定義節日列表，格式為 'YYYY-MM-DD'
holidays = ['2024-01-01', '2024-02-10', '2024-02-11', '2024-02-12', '2024-04-04', '2024-06-12', '2024-10-10', '2024-05-01', '2024-10-10', '2024-02-24', '2024-09-19', '2024-02-09']

# 將節日列表轉換為 datetime 對象
holidays = pd.to_datetime(holidays)

# 找出所有符合特定模式的檔案
files = glob.glob(r"C:\Users\WINNIE\Desktop\M05A\M05A_*.csv")

for file in files:
    print("Processing", file)
    # 檢查該檔案是否已經被轉換過
    if "_feature" in file or os.path.exists(file.replace(".csv", "_feature.csv")):
        continue  # 如果已經被轉換過，則跳過該檔案

    # 讀取 CSV 檔案
    df = pd.read_csv(file)

    # 將 TimeInterval 欄位的時間轉換為每天的第 n 個 5 分鐘
    df['OriginalTimeInterval'] = pd.to_datetime(df['TimeInterval'])
    df['TimeInterval'] = df['OriginalTimeInterval'].apply(lambda x: x.hour * 60 + x.minute) // 5

    # 新增欄位
    df['WeekDay'] = df['OriginalTimeInterval'].dt.dayofweek
    df['WeekDay'] = df['WeekDay'].apply(lambda x: (x + 1) % 7)  # 0 代表星期日，1 代表星期一，...，6 代表星期六

    # 檢查每一行的日期是否在節日列表中
    df['Holiday'] = df['OriginalTimeInterval'].dt.date.isin(holidays.date)

    # 如果是節日或者是週末，則將 HellDay 設為 1
    df['HellDay'] = df.apply(lambda row: 1 if row['Holiday'] or row['WeekDay'] >= 5 else 0, axis=1)

    # 刪除臨時欄位
    df = df.drop(columns=['Holiday'])

    df['WayIDFrom'] = df['GantryFrom'].apply(lambda x: x[:3])
    df['WayIDTo'] = df['GantryTo'].apply(lambda x: x[:3])
    df['WayMilageFrom'] = df['GantryFrom'].apply(lambda x: float(''.join(filter(str.isdigit, x[3:]))))
    df['WayMilageTo'] = df['GantryTo'].apply(lambda x: float(''.join(filter(str.isdigit, x[3:]))))
    df['WayDirectionFrom'] = df['GantryFrom'].apply(lambda x: x[-1])
    df['WayDirectionTo'] = df['GantryTo'].apply(lambda x: x[-1])

    # 使用 map 方法將門架方向的英文表示轉換為中文
    df['WayDirectionFrom'] = df['WayDirectionFrom'].map(direction_dict)
    df['WayDirectionTo'] = df['WayDirectionTo'].map(direction_dict)

    # 速度分級
    bins = [-np.inf, 0, 20, 40, 60, 80, np.inf]
    labels = [0, 1, 2, 3, 4, 5]
    df['SpeedClass'] = pd.cut(df['SpaceMeanSpeed'], bins=bins, labels=labels)

    # 儲存特徵化後的檔案
    df.to_csv(file.replace(".csv", "_feature.csv"), index=False)
print("All files have been processed.")