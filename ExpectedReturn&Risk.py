from Gather_Data import GatherData
import statistics
import pandas as pd

###
#Function takes input:
#   DataFrame of close and dividend values of any interval
#
#Output:
#List of yearly returns
#

def ExpectedReturn(Data):
    #convert index to desirable format
    Data.index.to_pydatetime()
    year = Data.index.year

    #init variables for 'for' loop
    curYear = year[0]
    curPrice = Data['Close'][0]
    curIndex = 0
    returns = []

    #Only check difference in prices for each year and sum dividends over that time
    for i in range(0, len(Data)):
        if(year[i] != curYear):
            dividends = sum(Data['Dividends'][curIndex:i])
            returns.append((Data['Close'][i] - curPrice) / curPrice + dividends/curPrice)
            curPrice = Data['Close'][i]
            curYear = year[i]
            curIndex = i

    return returns

def ExpectedReturnRisk(returns):
    return statistics.stdev(returns)

if __name__ == "__main__":
    Ticker = "ORG.AX"
    Period = "10y"
    Interval = "1d"
    closeData = GatherData(Ticker, Period, Interval)
    HistoricalReturn = statistics.mean(ExpectedReturn(closeData))
    HistoricalReturnRisk = ExpectedReturnRisk(ExpectedReturn(closeData))

    print(HistoricalReturn)
    print(HistoricalReturnRisk)
