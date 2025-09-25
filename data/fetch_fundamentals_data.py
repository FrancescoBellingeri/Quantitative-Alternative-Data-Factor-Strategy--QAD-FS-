import pandas as pd
from urllib.request import urlopen
import certifi
import json
import os
from dotenv import load_dotenv

load_dotenv()

FINANCIAL_MODELING_API_KEY = os.getenv('FINANCIAL_MODELING_API_KEY')

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "GOOGL", "META"]

for ticker in tickers:
    # URL API
    url_income_statement = f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter"
    url_balance_sheet_statement = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter"
    url_cash_flow_statement = f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FINANCIAL_MODELING_API_KEY}&period=quarter"

    # Otteniamo i dati
    df_income = pd.DataFrame(get_jsonparsed_data(url_income_statement))
    df_balance = pd.DataFrame(get_jsonparsed_data(url_balance_sheet_statement))
    df_cash = pd.DataFrame(get_jsonparsed_data(url_cash_flow_statement))

    # Selezioniamo solo le colonne che ci interessano
    df_income_sel = df_income[["date", "filingDate", "symbol", "netIncome", "eps", "weightedAverageShsOut"]]
    df_balance_sel = df_balance[["date", "symbol", "totalStockholdersEquity", "totalDebt", "netDebt"]]
    df_cash_sel = df_cash[["date", "symbol", "freeCashFlow", "operatingCashFlow"]]

    # Merge su 'date' e 'symbol'
    df_final = df_income_sel.merge(df_balance_sel, on=["date", "symbol"], how="inner") \
                            .merge(df_cash_sel, on=["date", "symbol"], how="inner")

    # Calcoli
    df_final["bookValuePerShare"] = df_final['totalStockholdersEquity'] / df_final['weightedAverageShsOut']
    df_final["ROE"] = df_final['netIncome'] / df_final['totalStockholdersEquity']
    df_final["debtToEquity"] = df_final['totalDebt'] / df_final['totalStockholdersEquity']

    # Ordiniamo per data decrescente
    df_final["date"] = pd.to_datetime(df_final["date"])
    df_final = df_final.sort_values("date", ascending=True)

    # Salviamo CSV senza indice
    df_final.to_csv(f"fundamental_data/{ticker}_fundamental_data.csv", index=False)
