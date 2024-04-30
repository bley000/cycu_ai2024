import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# 讀取CSV檔案
df = pd.read_csv('c:\\Users\\User\\Downloads\\TDCS_M03A_20240429_005500.csv')

# 將時間和地點轉換為數值
le = LabelEncoder()
df['時間'] = le.fit_transform(df['時間'])
df['地點'] = le.fit_transform(df['地點'])

# 選取小客車的數據
df = df[df['類別'] == 31]

# 將數據分為訓練集和測試集
X = df[['時間', '地點']]
y = df['數量']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 創建並訓練多項式迴歸模型
degree = 2
polyreg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
polyreg.fit(X_train, y_train)

# 使用模型預測測試集的中位數車速
y_pred = polyreg.predict(X_test)

# 繪製三維座標圖
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_test['時間'], X_test['地點'], y_pred, c=y_pred, cmap='viridis')
ax.set_xlabel('時間')
ax.set_ylabel('地點')
ax.set_zlabel('中位數車速')
plt.show()