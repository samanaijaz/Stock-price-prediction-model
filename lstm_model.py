# -*- coding: utf-8 -*-
"""LSTM Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q7X6sshEKAoLskCftTQHk87gVN5faog_

First of all, importing all necessary libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data

"""Importing yfinance for scrapping data from yahoo webiste. pandas_datareader could also have been used instead"""

import yfinance as yf

pip install streamlit

from keras.models import load_model
import streamlit as st

"""Defining the start and the end, bigger dataframe is preferred."""

start = '2010-01-01'
end = '2019-12-31'

#df = yf.download('AAPL', 'yahoo', start, end)
# Use yfinance to get the data

st.title('Stock Trend Predictor')
user_input = st.text_input('Enter Stock Ticker', 'AAPL')

df = yf.download(user_input, start=start, end=end)

#df.head()

##describing data
st.subheader('Data from 2010 - 2019')
st.write(df.describe())

##visualization
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

"""Removing date as index and then dropping the columns which we don't need"""

df = df.reset_index()
df.head()

df = df.drop(['Date', 'Adj Close'], axis = 1)
df.head()

"""I am interested in the closing price of the stocks thus I am analysing the Close column"""

df

"""Moving average is the average of a particular time frame."""

df.shape

df

df = df.reset_index()
df.head()

df = df.drop(['Date', 'Adj Close'], axis = 1)
df.head()

# Create a new dataframe with only the 'Close column
data = df.filter(['Close'])
# Convert the dataframe to a numpy array
dataset = data.values
# Get the number of rows to train the model on
training_data_len = int(np.ceil( len(dataset) * .95 ))

training_data_len

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

train_data = scaled_data[0:int(training_data_len), :]
# Split the data into x_train and y_train data sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i<= 61:
        print(x_train)
        print(y_train)
        print()

# Convert the x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
# x_train.shape

from keras.models import Sequential
from keras.layers import Dense, LSTM

# Build the LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)

model.save('keras_model.h5')

# Create the testing data set
# Create a new array containing scaled values from index 1543 to 2002
test_data = scaled_data[training_data_len - 60: , :]
# Create the data sets x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])

# Convert the data to a numpy array
x_test = np.array(x_test)

# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

# Get the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Get the root mean squared error (RMSE)
rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
rmse

plt.figure(figsize =(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(predictions, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()