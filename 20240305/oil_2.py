import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    data_frames = [pd.read_html(str(table))[0] for table in tables]
    return pd.concat(data_frames)

url1 = 'https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx'
url2 = 'https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil2019.aspx'

data1 = get_data(url1)
data2 = get_data(url2)

data = pd.concat([data1, data2])

data.to_csv('C:/Users/USER/Desktop/oil_prices.csv', index=False)
print(data)
#將NAN值去除
data = data.dropna()
#只保留前5個欄位的資料
data = data.iloc[:, :5]



#將第一欄的資料型態轉成datetime
data[data.columns[0]] = pd.to_datetime(data[data.columns[0]])
print(data)

#以matplotlib繪製折線圖 以日期為x軸 油價為y軸
import matplotlib.pyplot as plt
#設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
# 使用 matplotlib x,y 折線圖 , x 軸是日期 , 後面四個欄位是 油價 ，分別是 92無鉛汽油,95無鉛汽油,98無鉛汽油,超級柴油 
plt.figure(figsize=(60, 6))
plt.plot(data[data.columns[0]], data[data.columns[1]], label='92無鉛汽油')
plt.plot(data[data.columns[0]], data[data.columns[2]], label='95無鉛汽油')
plt.plot(data[data.columns[0]], data[data.columns[3]], label='98無鉛汽油')
plt.plot(data[data.columns[0]], data[data.columns[4]], label='超級柴油')
plt.legend()
plt.xticks(rotation=45)
plt.xticks(data[data.columns[0]][::30])
plt.show()
