import pandas as pd

# 讀取 CSV 檔案
df1 = pd.read_csv("C:\\Users\\WINNIE\\Desktop\\M05.csv")
df2 = pd.read_csv("C:\\Users\\WINNIE\\Desktop\\M03.csv")

# 合併 DataFrame 物件
merged_df = pd.concat([df1, df2])

# 寫入新的 CSV 檔案
merged_df.to_csv("C:\\Users\\WINNIE\\Desktop\\merged.csv", index=False)