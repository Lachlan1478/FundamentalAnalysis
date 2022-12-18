

pacman::p_load(data.table, tidyverse, dplyr)
company_data <- read.csv("sortbyPE.csv")
company_data <- data.table(company_data)

#Keep copy of original dataset
original_data <-company_data

#Add index for marketCap
company_data <- company_data[!is.na(marketCap)]
company_data <- company_data[order(-marketCap)]

company_data[, `:=` (marketCap_index = order(-marketCap))]
top_ten <- company_data[1:10]

#sort by forwardPE
company_data <- company_data[order(forwardPE)]

#remove companies with PE less than 0
company_data <- company_data[forwardPE>0]

#remove companies with operatingcashFlow less than 0
company_data <- company_data[operatingCashflow > 0, ]

#top 50 companies by PE
company_data <- company_data[1:50]

company_data <- company_data[order(marketCap_index)]


