import pandas as pd
import numpy as np
from scipy.stats import jarque_bera
import matplotlib.pyplot as plt
from coinpaprika import client as Coinpaprika
from statsmodels.tsa.arima.model import ARIMA


client = Coinpaprika.Client()


raw = client.historical(
"eth-ethereum", start="2023-01-11T00:00:00Z", limit=5000, interval='1m')
df = pd.DataFrame(raw)


df = df[['timestamp', 'price']]
df.columns = ['date', 'price']




# Calculate log returns
df['LogReturns'] = np.log(df['price'] / df['price'].shift(periods=1))
y = df['LogReturns']


# Compute quadratic variation
QV = []
for i in range(10, len(y), 10):
    QV.append(np.sum(np.diff(y[i-10:i])**2))
QV = pd.Series(QV)

# Standardize
z = (QV - QV.mean()) / QV.std()


model = ARIMA(z, order=(2,1,2))
results = model.fit()

# result.summary() to see more details

_, ax = plt.subplots()


ax.plot(df['price'], label='Exchange Rate')


ax.set_xlabel('Date')
ax.set_ylabel('Exchange Rate (ETH/USD)')
ax.legend()


_, ax2 = plt.subplots()


ax2.plot(z, label='Quadratic Variation')


ax2.set_xlabel('Periods')
ax2.set_ylabel('Quadratic Variation (ETH/USD)')
ax2.legend()

#plt.show()

