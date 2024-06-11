import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 文件路徑
file_path = "/workspaces/cycu_ai2024/空氣品質與交通量.xlsx"

# 讀取Excel文件的第二個工作表
df = pd.read_excel(file_path, sheet_name=0)

# 提取日期和空氣品質數據
dates = df.iloc[:, 1].values
pm25_data = df.iloc[:, 3].astype(float).values

# 將日期時間戳轉換為數值
date_nums = [mdates.date2num(date) for date in dates]

# 繪製折線圖
plt.figure(figsize=(10, 5))
plt.plot_date(date_nums, pm25_data, label='PM2.5', fmt='-o')

# 設置圖表標題和圖例
plt.title('PM2.5 Data')
plt.xlabel('Date')
plt.ylabel('PM2.5')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#將圖片另存為圖片檔
plt.savefig('pm25_data.png')