import requests
import pandas as pd
from datetime import datetime as dt
from datetime import UTC
import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket_name = os.getenv('gabsmarqs-bucket', 'my-default-bucket')
        file_name = f"data/coin-info-{dt.now().strftime('%Y-%m-%dT%H:%M:%S')}.json"
        content = get_json_data()

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=content,
            ContentType='application/json'
        )

        logger.info(f"Arquivo {file_name} enviado para o bucket {bucket_name} com sucesso.")
        return {
            'statusCode': 200,
            'body': json.dumps('Arquivo enviado com sucesso!')
        }
    except Exception as e:
        logger.error(f"Erro ao processar a função: {e}")
        raise e

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

        # Converter timestamp Unix para datetime e formatar
        timestamp = bitcoin_data['last_updated_at']
        data_formatada = dt.fromtimestamp(timestamp, UTC).strftime('%Y-%m-%dT%H:%M:%S')
        
        df = pd.DataFrame({
            'moeda': ['bitcoin', 'ethereum'],
            'valor': [bitcoin_data['brl'], ethereum_data['brl']],
            'data_coleta': [data_formatada, data_formatada]  # Mesmo timestamp para ambas
        })
        
        df['valor'] = df['valor'].astype(float).round(2)

        # Ajustar o fuso horário para UTC-3
        df['data_coleta'] = pd.to_datetime(df['data_coleta']) 
        df['data_coleta'] = df['data_coleta'] - pd.Timedelta(hours=3)
        df['data_coleta'] = df['data_coleta'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        return df

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return pd.DataFrame()

def get_dolar_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data = data['USDBRL']

        # Converter a string de data para formato ISO
        data_str = data['create_date']
        try:
            # Tentar parsear o formato original
            data_dt = dt.strptime(data_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Se falhar, tentar outro formato comum
            data_dt = dt.strptime(data_str, '%d/%m/%Y %H:%M:%S')
        
        data_formatada = data_dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        df = pd.DataFrame({
            'moeda': ['dolar'],
            'valor': [float(data['bid'])],
            'data_coleta': [data_formatada]
        })

        df['valor'] = df['valor'].astype(float).round(2)

        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return pd.DataFrame()

def get_json_data():
    # Obtendo os dados
    bitcoin_df = get_bitcoin_data()
    dolar_df = get_dolar_data()

    # Concatenando os DataFrames
    df = pd.concat([bitcoin_df, dolar_df], ignore_index=True)

    json_data = df.to_json(orient='records', indent=4, force_ascii=False)

    return json_data

