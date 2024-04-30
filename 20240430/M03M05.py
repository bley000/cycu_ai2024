import pandas as pd

# 讀取CSV檔案
df1 = pd.read_csv('c:\\Users\\User\\Desktop\\traffic.csv')
df2 = pd.read_csv('c:\\Users\\User\\Desktop\\M05.csv')

# 直接合併兩個檔案
merged_df = pd.concat([df1, df2])

# 將缺失值填入'NA'
merged_df.fillna('NA', inplace=True)

# 儲存合併後的資料
merged_df.to_csv('c:\\Users\\User\\Desktop\\merged.csv', index=False)