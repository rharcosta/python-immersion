# -*- coding: utf-8 -*-
"""Forecasting_TimeSeries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Md1mzPJjw_XafCh5KbvUg_inrd7cZgRM

# Importing libraries
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

"""# Downloading the Johnson&Johnson share"""

data = yf.download("JNJ", start = '2020-01-01', end = '2023-12-31', progress = False) #progress = progress bar
data = data.reset_index()

"""# Separating data in training and testing"""

data_train = data[data['Date'] < '2023-07-31']
data_test = data[data['Date'] >= '2023-07-31']

"""# Preparing the train data"""

#from training data, we will take the Date and the Close value that will be renamed by ds and y
data_prophet_train = data_train[['Date', 'Close']].rename(columns = {'Date':'ds', 'Close':'y'})
data_prophet_train

"""# Creating and Training the model"""

#I'm saying to the model to pay attention on weekly and yearly seasonality
model = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False)

#including the holidays of US because the share JNJ is from US
model.add_country_holidays(country_name = 'US')

#learn and adjust
model.fit(data_prophet_train)

"""# Creating future dates to test the model"""

future = model.make_future_dataframe(periods = 150)
forecast = model.predict(future)
forecast

"""# Creating graphics for the model"""

#defining the size of the graphic
plt.figure(figsize = (14, 8))

#plotting the train and test data (Date = x; Close = y)
plt.plot(data_train['Date'], data_train['Close'], label = 'Train Data', color = 'blue')
plt.plot(data_test['Date'], data_test['Close'], label = 'Test Data', color = 'green')

#plotting the future data
plt.plot(forecast['ds'], forecast['yhat'], label = 'Forecast', color = 'orange', linestyle = '--')

#creating a vertical line to show the start of forecast
plt.axvline(data_train['Date'].max(), color = 'red', label = 'Start of Forecast', linestyle = '--')

#setting labels
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Forecast of Closing Price vs Real Data')

#showing the labels
plt.legend()

#showing the graphic
plt.show()