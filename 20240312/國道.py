import pandas as pd


#得到這個檔案 __file__ 是這個檔案的路徑
import os
path = os.path.abspath(__file__)
#get the folder of this file
path = os.path.dirname(path)


# 從 Excel 文件讀取數據
excel_file = 'c:\\Users\\User\\Desktop\\112年1-10月交通事故簡訊通報資料.xlsx'

filepath = os.path.join(path ,excel_file)

# 讀取 Excel 文件
df = pd.read_excel(filepath, sheet_name='交通事故簡報通報資料')

# Filter the data for '國道名稱' is '國道1號' and '方向' is '南' or '南下'
df1 = df.loc[(df['國道名稱'] == '國道1號') & ((df['方向'] == '北') | (df['方向'] == '北向'))]

#把 欄位 '年' '月' '日' '時' '分'
#合併成一個欄位 '日期' , 並且轉換成日期格式
df1['事件開始'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['時'].astype(str) + ':' + df1['分'].astype(str)
df1['事件開始'] = pd.to_datetime(df1['事件開始'])

#把 欄位 '年' '月' '日' '事件排除'  合併成一個欄位 '事件排除' , 並且轉換成日期格式
df1['事件排除'] = df1['年'].astype(str) + '-' + df1['月'].astype(str) + '-' + df1['日'].astype(str) + ' ' + df1['事件排除'].astype(str)
df1['事件排除'] = pd.to_datetime(df1['事件排除'])

#drop 欄位 '年' '月' '日' '時' '分'
df1 = df1.drop(columns=['年', '月', '日', '時', '分'])


#將 '事件開始' '事件排除' 兩個欄位轉換成 unix time stamp 並使用整數表示
import pandas as pd

# 假設 df 是您的 DataFrame，並且 '事件開始' 和 '事件排除' 是 datetime 欄位

df1['事件開始1'] = df1['事件開始'].apply(lambda x: int(x.timestamp()))
df1['事件排除1'] = df1['事件排除'].apply(lambda x: int(x.timestamp()))

#只印出 '事件開始' '事件排除' '國道名稱' '事件類型' '事件描述'
print(df1[['事件開始', '事件排除', '國道名稱','里程','事件開始1','事件排除1']])

import matplotlib.pyplot as plt
import matplotlib

# 設定支援中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
matplotlib.rcParams['axes.unicode_minus'] = False

# 假設 df 是您的 DataFrame
for index, row in df1.iterrows():
    plt.plot([row['事件開始1'], row['事件排除1']], [row['里程'], row['里程']])

plt.xlabel('事件時間')
plt.ylabel('里程')
plt.title('11022201國道1號北上')
plt.show()