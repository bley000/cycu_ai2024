import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# 獲取網頁內容
response = requests.get('https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx')

# 解析網頁內容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有的表格元素
tables = soup.find_all('table')

# 將 HTML 表格轉換為 DataFrame
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]

# 將 DataFrame 寫入 CSV 檔案
df2.to_csv("C:/Users/USER/Desktop/oil.csv", index=False)

# df2 只保留前5個欄位的資料
df2 = df2[df2.columns[:5]]

# 使用前一個值填充NaN
df2 = df2.fillna(method='ffill')

# 把第一欄的資料型態 轉成 datetime
df2[df2.columns[0]] = pd.to_datetime(df2[df2.columns[0]])

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 使用 matplotlib 繪製折線圖 , x 軸是日期 , y 軸是無鉛汽油92
plt.plot(df2[df2.columns[0]], df2[df2.columns[1]],'y')

# 使用 matplotlib 繪製折線圖 , x 軸是日期 , y 軸是無鉛汽油95
plt.plot(df2[df2.columns[0]], df2[df2.columns[2]],'g')

# 使用 matplotlib 繪製折線圖 , x 軸是日期 , y 軸是無鉛汽油98
plt.plot(df2[df2.columns[0]], df2[df2.columns[3]],'b')

# 使用 matplotlib 繪製折線圖 , x 軸是日期 , y 軸是超級/高級柴油
plt.plot(df2[df2.columns[0]], df2[df2.columns[4]],'c')

#將四條折線圖放在一張圖上
plt.legend(['無鉛汽油92', '無鉛汽油95', '無鉛汽油98', '超級/高級柴油'])

# 顯示圖片
plt.show()
plt.savefig("C:/Users/USER/Desktop/oil.png")