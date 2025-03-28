import requests
import pandas as pd
from datetime import datetime as dt

def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "brl",
        "include_last_updated_at": "true"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        bitcoin_data = data['bitcoin']
        ethereum_data = data['ethereum']

        df = pd.DataFrame({
            'bitcoin_price': [bitcoin_data['brl']],
            'ethereum_price': [ethereum_data['brl']]
        })
        
        return df

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def get_dolar_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data = data['USDBRL']

        df = pd.DataFrame({
            'dolar_price': [data['bid']]
        })

        df['dolar_price'] = df['dolar_price'].astype(float).round(2)

        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

bitcoin_df = get_bitcoin_data()
dolar_df = get_dolar_data()

df = pd.merge(bitcoin_df, dolar_df, left_index=True, right_index=True)

df['updated_at'] = dt.now().strftime('%d/%m/%Y %H:%M:%S')

print(df)
