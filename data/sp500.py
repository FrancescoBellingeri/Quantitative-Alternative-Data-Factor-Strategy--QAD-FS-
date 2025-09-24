import pandas as pd
import requests

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Alza eccezione se c'è errore HTTP

# Ora usa pandas per leggere il contenuto HTML già scaricato
df = pd.read_html(response.text)[0]

tickers = df['Symbol'].tolist()
df.to_csv("data/sp500_tickers.csv", index=False)

