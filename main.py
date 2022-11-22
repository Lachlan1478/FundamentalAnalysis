
import pandas as pd
import yfinance as yf
import Gather_Data
import ExpectedReturnRisk as Ex
import statistics

Companies = ['ORG.AX', 'WDS.AX']
Metrics = ['trailingEps', 'forwardEps', 'enterpriseToRevenue', 'ebitda', 'returnOnAssets',
           'returnOnEquity', 'debtToEquity', 'heldPercentInstitutions', 'priceToBook',
           'enterpriseValue', 'marketCap', 'operatingCashflow', 'averageVolume']
CompanyMetrics = {}

for company in Companies:

    CompanyMetrics[company] = {}
    CompanyInfo = yf.Ticker(company)

    for metric in Metrics:
        try:
            CompanyMetrics[company][metric] = CompanyInfo.info[metric]
        except:
            CompanyMetrics[company][metric] = "NA"

    try:
        CompanyPrice = Gather_Data.GatherData(company, "1d", "1d")["Close"][0]
        CompanyMetrics[company]['PricePerShare'] = CompanyPrice
        CompanyMetrics[company]['trailingPE'] = CompanyMetrics[company]['PricePerShare'] / CompanyMetrics[company]['trailingEps']
        CompanyMetrics[company]['forwardPE'] = CompanyMetrics[company]['PricePerShare'] / CompanyMetrics[company]['forwardEps']
    except:
        CompanyMetrics[company]['trailingPE'] = "NA"
        CompanyMetrics[company]['forwardPE'] = "NA"

    try:
        closeData = Gather_Data.GatherData(company, "10y", "1d")
        CompanyMetrics[company]['HistoricalReturn'] = statistics.mean(Ex.ExpectedReturn(closeData))
        CompanyMetrics[company]['HistoricalReturnRisk'] = Ex.ExpectedReturnRisk(Ex.ExpectedReturn(closeData))
    except:
        CompanyMetrics[company]['HistoricalReturn'] = "NA"
        CompanyMetrics[company]['HistoricalReturnRisk'] = "NA"

df = pd.DataFrame.from_dict(CompanyMetrics).T
print(df)

sortbyPE = df.sort_values(by = 'forwardPE')
print(sortbyPE)
df.to_csv('sortbyPE.csv')
