import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from datetime import date
import dateutil.relativedelta

en=date.today()
st = en - dateutil.relativedelta.relativedelta(months=2)
df = yf.download("AMZN",st,en)
df.reset_index(inplace=True)
print(df.head())

df=df[['Adj Close']]
print(df.head())

forecast_out=30
df['Prediction']=df[['Adj Close']].shift(-forecast_out)
print(df.head())

X=np.array(df.drop(['Prediction'],1))
X=X[:-forecast_out]
print(X)

Y=np.array(df['Prediction'])
Y=Y[:-forecast_out]
print(Y)

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2)

svr_rbf=SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_rbf.fit(x_train,y_train)

svm_confidence=svr_rbf.score(x_test,y_test)
print("svm confidence: ", svm_confidence)

lr=LinearRegression()
lr.fit(x_train,y_train)

lr_conf=lr.score(x_test,y_test)
print("lr conf:",lr_conf)

x_forecast=np.array(df.drop(['Prediction'],1))[-forecast_out:]
print(x_forecast)

lr_prediction=lr.predict(x_forecast)
print(lr_prediction)

svm_prediction=svr_rbf.predict(x_forecast)
print(svm_prediction)