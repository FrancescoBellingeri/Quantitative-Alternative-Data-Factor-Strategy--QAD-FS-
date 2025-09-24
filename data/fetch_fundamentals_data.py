import requests
import pandas as pd

API_KEY = "7K1VeM6l7bLe2xy3vA1uHZylZ1ENqPRL"
url = f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?limit=40&apikey={API_KEY}"
inc = pd.DataFrame(requests.get(url).json())
inc['reportDate'] = pd.to_datetime(inc['date'])
inc.to_parquet("raw/fmp_income_AAPL.parquet", index=False)
