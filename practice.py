# Import necessary libraries
import streamlit as st
import yfinance as yf
from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

# Download stock data
stock_data = yf.download('AAPL', start='2010-01-01', end='2024-04-16')

# Analyze stock data
st.subheader('Stock Data')
st.write(stock_data.head(50))

# Clean data
stock_data = stock_data[['Close']]

# Prepare data for Prophet
df = stock_data.reset_index()
df = df.rename(columns={'Date': 'ds', 'Close': 'y'})

# Train Prophet model
model = Prophet()
model.fit(df)

# Make future predictions
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Plot Prophet results
fig = model.plot(forecast)
st.pyplot(fig)

# Calculate daily returns
returns = stock_data.Close.pct_change()

# Analyze daily returns
st.subheader('Daily Returns')
st.write(returns.head(50))

# Clean and prepare data for machine learning
X = returns.values
X = X.reshape(-1, 1)
X = np.nan_to_num(X)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, X, test_size=0.2, random_state=0)

# Train machine learning model
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(n_estimators=100, random_state=0)
rf_model.fit(X_train, y_train)

# Evaluate machine learning model
rf_predictions = rf_model.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_predictions)
rf_mse = mean_squared_error(y_test, rf_predictions)

# Display evaluation metrics
st.write(f'Random Forest MAE: {rf_mae}')
st.write(f'Random Forest MSE: {rf_mse}')