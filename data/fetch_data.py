from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta, timezone
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('API_SECRET')

tickers_df = pd.read_csv('data/sp500_tickers.csv')

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# Definiamo un periodo storico specifico per il backtesting
end_date = datetime(2025, 9, 23)
start_date = datetime(2016, 1, 1)   # Dall'inizio del 2016

try:
    for index, row in tickers_df.iterrows():
        request_params = StockBarsRequest(
            symbol_or_symbols=row['Symbol'],
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date
        )

        bars = client.get_stock_bars(request_params)
        df = bars.df
        
        # Pulizia e preparazione dei dati
        if isinstance(df.index, pd.MultiIndex):
            df = df.reset_index()
        
        # Opzionale: salva i dati in un file CSV
        df.to_csv(f'data/{row['Symbol']}_daily.csv', index=False)
        print(f"\nDati salvati in '{row['Symbol']}_daily.csv'")
        

except Exception as e:
    print(f"Errore: {e}")