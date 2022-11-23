
import pandas as pd
import yfinance as yf
import Gather_Data
import ExpectedReturnRisk as Ex
import statistics
import numpy as np

Path = "ALLORDS_Tickers.txt"

Read = open(Path, "r")
for i in Read:
    Tickers = [line.strip('"'+'\n') for line in open(Path)]

Length = len(Tickers)
for i in range(0, Length):
    Tickers[i] = Tickers[i]+'.AX'


#Companies = ['ORG.AX', 'WDS.AX']

Metrics = ['trailingEps', 'forwardEps', 'enterpriseToRevenue', 'ebitda', 'returnOnAssets',
           'returnOnEquity', 'debtToEquity', 'heldPercentInstitutions', 'priceToBook',
           'enterpriseValue', 'marketCap', 'operatingCashflow', 'averageVolume']
CompanyMetrics = {}
i = 0
for company in Tickers:
    print("Iteration ", i, ": begin")

    CompanyMetrics[company] = {}
    CompanyInfo = yf.Ticker(company)

    for metric in Metrics:
        try:
            CompanyMetrics[company][metric] = CompanyInfo.info[metric]
        except:
            CompanyMetrics[company][metric] = np.nan

    try:
        CompanyPrice = Gather_Data.GatherData(company, "1d", "1d")["Close"][0]
        CompanyMetrics[company]['PricePerShare'] = CompanyPrice
        CompanyMetrics[company]['trailingPE'] = CompanyMetrics[company]['PricePerShare'] / CompanyMetrics[company]['trailingEps']
        CompanyMetrics[company]['forwardPE'] = CompanyMetrics[company]['PricePerShare'] / CompanyMetrics[company]['forwardEps']
    except:
        CompanyMetrics[company]['trailingPE'] = np.nan
        CompanyMetrics[company]['forwardPE'] = np.nan

    try:
        closeData = Gather_Data.GatherData(company, "10y", "1d")
        CompanyMetrics[company]['HistoricalReturn'] = statistics.mean(Ex.ExpectedReturn(closeData))
        CompanyMetrics[company]['HistoricalReturnRisk'] = Ex.ExpectedReturnRisk(Ex.ExpectedReturn(closeData))
    except:
        CompanyMetrics[company]['HistoricalReturn'] = np.nan
        CompanyMetrics[company]['HistoricalReturnRisk'] = np.nan
    print("Iteration ", i, ": end")
    i = i+1

df = pd.DataFrame.from_dict(CompanyMetrics).T

sortbyPE = df.sort_values(by = 'forwardPE')
print(sortbyPE)
df.to_csv('sortbyPE.csv')
