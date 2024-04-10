import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from image import ImageApp


# Function to fetch coin data using the provided API key
def get_coin_data(coin_name, days):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days={days}"
        headers = {
          "accept": "application/json",
          "x-cg-demo-api-key": "CG-RkTJDcUzivMK8Uq1vFGpFEKS"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.RequestException as e:
        st.error("Error fetching data. Please enter valid coin name.")
        return None

def plot_price_comparison(df1, df2, coin1_name, coin2_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df1['timestamp'], df1['price'], label=coin1_name, marker='o', linestyle='-')
    plt.plot(df2['timestamp'], df2['price'], label=coin2_name, marker='o', linestyle='-')
    plt.title('Price Comparison')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot()

def max_min_price_comparison(df1, df2, coin1_name, coin2_name):
    max_price_1 = df1['price'].max()
    min_price_1 = df1['price'].min()
    max_date_1 = df1[df1['price'] == max_price_1]['timestamp'].iloc[0]
    min_date_1 = df1[df1['price'] == min_price_1]['timestamp'].iloc[0]
    st.write(f"Maximum price for {coin1_name}: ${max_price_1:.2f} on {max_date_1}")
    st.write(f"Minimum price for {coin1_name}: ${min_price_1:.2f} on {min_date_1}")
    
    max_price_2 = df2['price'].max()
    min_price_2 = df2['price'].min()
    max_date_2 = df2[df2['price'] == max_price_2]['timestamp'].iloc[0]
    min_date_2 = df2[df2['price'] == min_price_2]['timestamp'].iloc[0]
    st.write(f"Maximum price for {coin2_name}: ${max_price_2:.2f} on {max_date_2}")
    st.write(f"Minimum price for {coin2_name}: ${min_price_2:.2f} on {min_date_2}")


def plot_price(df):
  plt.figure(figsize=(10, 6))
  plt.plot(df['timestamp'], df['price'], marker='o', linestyle='-')
  plt.title('Price Over Last Year')
  plt.xlabel('Date')
  plt.ylabel('Price (USD)')
  plt.grid(True)
  st.pyplot()

def max_min_price(df):
  max_price = df['price'].max()
  min_price = df['price'].min()
  max_date = df[df['price'] == max_price]['timestamp'].iloc[0]
  min_date = df[df['price'] == min_price]['timestamp'].iloc[0]
  st.write(f"Maximum price: ${max_price:.2f} on {max_date}")
  st.write(f"Minimum price: ${min_price:.2f} on {min_date}")

def app1():
    st.title('Cryptocurrency Stock Details')

    coin_name = st.text_input("Enter a cryptocurrency name:")
    if st.button('Get Details'):
        if coin_name:  
            st.write(f"Fetching details for {coin_name}...")
            df = get_coin_data(coin_name, 365)  
            if df is not None:
                plot_price(df)
                max_min_price(df)
        else:
            st.warning("Please enter a cryptocurrency name.")

def app2():
    st.title('Cryptocurrency Stock Comparison')
    

    coin1_name = st.text_input("Enter the first cryptocurrency name:")
    coin2_name = st.text_input("Enter the second cryptocurrency name:")
    timeframe = st.selectbox("Select the timeframe:", ["1 week", "1 month", "1 year"])

    if st.button('Compare'):
        if coin1_name and coin2_name:
            st.write(f"Fetching details for {coin1_name} and {coin2_name}...")
            if timeframe == "1 week":
                days = 7
            elif timeframe == "1 month":
                days = 30
            elif timeframe == "1 year":
                days = 365
                
            df1 = get_coin_data(coin1_name, days)
            df2 = get_coin_data(coin2_name, days)
            
            if not df1.empty and not df2.empty:
                plot_price_comparison(df1, df2, coin1_name, coin2_name)
                max_min_price_comparison(df1, df2, coin1_name, coin2_name)
            else:
                st.warning("Please enter valid cryptocurrency names.")
        else:
            st.warning("Please enter cryptocurrency names.")

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.sidebar.title('Navigation')
    app_selection = st.sidebar.radio("Go to", ('Cryptocurrency Stock Details', 'Cryptocurrency Stock Comparison','Image Classifier'))

    if app_selection == 'Cryptocurrency Stock Details':
        app1()
    elif app_selection == 'Cryptocurrency Stock Comparison':
        app2()
    elif app_selection == 'Image Classifier':
        image_app = ImageApp()
        image_app.main()

if __name__ == "__main__":
    main()
