import pandas as pd
from urllib.request import urlopen
import certifi
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

FINANCIAL_MODELING_API_KEY = os.getenv('FINANCIAL_MODELING_API_KEY')

def get_jsonparsed_data(url):
    try:
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        print(f"Errore nella richiesta a {url}")
        return []

tickers_df = pd.read_csv('data/sp500_tickers.csv')

for index, row in tickers_df.iterrows():
    try:
        # URL API
        ticker = row['Symbol']

        if os.path.isfile(f'fundamental_data/{ticker}_fundamental_data.csv'):
            continue

        url_income_statement = f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter&limit=40"
        url_balance_sheet_statement = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter&limit=40"
        url_cash_flow_statement = f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter&limit=40"

        # Otteniamo i dati
        df_income = pd.DataFrame(get_jsonparsed_data(url_income_statement))
        df_balance = pd.DataFrame(get_jsonparsed_data(url_balance_sheet_statement))
        df_cash = pd.DataFrame(get_jsonparsed_data(url_cash_flow_statement))

        # Selezioniamo solo le colonne che ci interessano
        df_income_sel = df_income[["date", "filingDate", "symbol", "netIncome", "eps", "weightedAverageShsOut", "revenue", "ebitda"]]
        df_balance_sel = df_balance[["date", "symbol", "totalStockholdersEquity", "totalDebt", "netDebt", "cashAndCashEquivalents"]]
        df_cash_sel = df_cash[["date", "symbol", "freeCashFlow", "operatingCashFlow"]]

        # Merge su 'date' e 'symbol'
        df_final = df_income_sel.merge(df_balance_sel, on=["date", "symbol"], how="inner") \
                                .merge(df_cash_sel, on=["date", "symbol"], how="inner")

        # Calcoli
        df_final["bookValuePerShare"] = df_final['totalStockholdersEquity'] / df_final['weightedAverageShsOut']
        df_final["ROE"] = df_final['netIncome'] / df_final['totalStockholdersEquity']
        df_final["ROA"] = df_final['netIncome'] / df_balance['totalAssets']

        nopat = df_income['ebit'] * (1 - df_income["incomeTaxExpense"] / (df_income["incomeBeforeTax"]))
        investedCapital = df_final["totalDebt"] + df_final["totalStockholdersEquity"] - df_final["cashAndCashEquivalents"]
        df_final["ROIC"] = nopat / investedCapital

        df_final["debtToEquity"] = df_final['totalDebt'] / df_final['totalStockholdersEquity']

        # Ordiniamo per data decrescente
        df_final["date"] = pd.to_datetime(df_final["date"])
        df_final = df_final.sort_values("date", ascending=True)

        # Salviamo CSV senza indice
        df_final.to_csv(f"fundamental_data/{ticker}_fundamental_data.csv", index=False)
        time.sleep(2)
    except Exception as e:
        print(f"Errore durante l'elaborazione di {ticker}")
        continue
