import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    data_frames = [pd.read_html(str(tables[1]))[0]]
    return pd.concat(data_frames)

url1 = 'https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx'
url2 = 'https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil2019.aspx'

data1 = get_data(url1)
data2 = get_data(url2)

#將data1和data2合併
data = pd.concat([data1, data2])
data.to_csv('C:/Users/USER/Desktop/oil_prices.csv', index=False)
#只留下data前五個欄位
data = data.iloc[:, :5]

#去除值是NaN的資料
data = data.dropna()

#以matplotlib繪製折線圖
import matplotlib.pyplot as plt

#文字修正
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

#設定index
data.set_index(data.columns[0], inplace=True)
data.plot(figsize=(20, 6))  # 在這裡調整圖表大小
plt.xticks(rotation=45)
plt.show()