# DESCRIPTION OF ANALYSIS:
# WE will focus our analysis on the relationship between weed prices in the State of California and observed number of crimes in 2 cities: San Francisco and LA
# We will explore variation of these 2 variables withtin the year 2014,
# First analysis: 1. how these variables behave from month to month within each city, how do they variate from month to month aggregating crime data for both cities.
# Second analysis: 2. is there a statistical association in the variation of number of crime incidents and weed prices within each city, on the aggregate?
# Data sources: A. Crime data SF (2014):
#               B. Crime data LA (2014):
#               C. California weed prices (2014):
# Methods:
#               First analysis: plot # number of crime incidents versus months within each city and overall
#                               plot weed prices versus months within each city and overall
#               Second Analysis: OLS regression weed prices (month average) on number of crime incidents (count on months) for each city + regplot for each city
#                                OLS regression "..." for aggregated data on crime + regplot for aggregated dat on crime

#0. Merging Datasets & creating dataframes for analysis
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plot
import seaborn as sns
from scipy import stats
import statsmodels.formula.api as sm

#0.1 MERGE CALIFRONIA WEED PRICES AND SAN FRANCISCO CRIME RATES
#0.1.1 Marihuana Dataframes
#MH_overall = pd.read_csv("marijuana-street-price-clean.csv",  index_col = 'date', parse_dates = ['date'])
MH_Cal = pd.read_csv("Californiaprices.csv", index_col = 'date', parse_dates =['date']) #See scrappginng and cleaning code of how we got to these Dataset
# plotting california weed prices trend
MH_Cal.rename(columns = {"MedQ" : "Price of Medium Quality"}, inplace = True)
priceplot= MH_Cal_df.plot(y = "Price of Medium Quality", use_index=True)
priceplot.set_ylabel("Daily Price of Medium Quality Marijuana")
priceplot.set_xlabel("Month")

#0.1.2 Crime Dataframes SF

C_SF = pd.read_csv("SF_crime_data_2014.csv", index_col = 'Date', parse_dates = ['Date']) # See scrappinng and cleaning code of how we got to these Dataset
#LA = pd.read_csv("LA_Crimes_2012-2015.csv", index_col = 'Date.Rptd', parse_dates = ['Date.Rptd'])

#0.1.3 Merge Califronia weed prices and SF crime rates

SF_merged = MH_Cal.join(C_SF)
SF_merged.to_csv('merged_Cal_SF.csv', index=False)


#1. Cleaning and slicing merged Dataset SF_merged
#1.1 Restrict to homicide categories (for now we are not considering all types of crime, only homicide attempts)
#Categories of homicide on data set: ATTEMPTED HOMICIDE WITH A GUN, ATTEMPTED HOMICIDE WITH A KNIFE, ATTEMPTED HOMICIDE WITH BODILY FORCE, ATTEMPTED HOMICIDE WITH A DANGEROUS WEAPON
homicides = SF_merged[(SF_merged['Descript'] == "ATTEMPTED HOMICIDE WITH A GUN") | (SF_merged['Descript'] == "ATTEMPTED HOMICIDE WITH A KNIFE") | (SF_merged['Descript'] == "ATTEMPTED HOMICIDE WITH BODILY FORCE") | (SF_merged['Descript'] == "ATTEMPTED HOMICIDE WITH A DANGEROUS WEAPON")]
homicides[:10]
#Pivot tables
#cathomicides = homicides.pivot_table(index='Descript', columns='Date', values='pdid', aggfunc=len)
#1.2 Deleting not useful columns : 'State',  'HighQ',  'HighQN',  'LowQ',  'LowQN', 'Category', 'Descript', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address'
del homicides['State']
del homicides['HighQ']
del homicides['HighQN']
del homicides['LowQ']
del homicides['LowQN']
del homicides['Category']
del homicides['Descript']
del homicides['DayOfWeek']
del homicides['Resolution']
del homicides['Address']
del homicides['PdDistrict']

#2.0 Dataframes for analysis SF
#2.1 Group by date, count by IncNumber
hom_count=homicides.groupby([homicides.index])[['IncidntNum']].count()
#2.2 Group by date, mean(price)
price_daily=homicides.groupby([homicides.index])[['MedQ']].mean()
reg_df = hom_count.join(price_daily)
#2.3 parse months
reg_df['month'] = pd.DatetimeIndex(reg_df.index).month
reg_df.to_csv('date_price_countH_month.csv', index=True)

#2.4 Group by month, count IncdNUmb, mean(prices)
month_price=reg_df.groupby(['month'])[['MedQ']].mean()
month_hom=reg_df.groupby(['month'])[['IncidntNum']].count()
month_merge= month_price.join(month_hom) #Rename y axis to "Number of Homicides"
month_merge
#3.1 First Analysis SF
month_merge.plot(kind="bar",  x=month_merge.index, y="IncidntNum")
fig_2 =plot.pyplot.gcf()
fig_2.savefig('fig_2.png')
month_merge.plot(kind="bar",  x=month_merge.index, y="MedQ").set_ylim(189, 194)
fig_3 =plot.pyplot.gcf()
fig_3.savefig('fig_3.png')

#3.2 Second Analysis SF : plot montly price with monthly count of homicides
fig, ax = plot.subplots()
sns.regplot(data = month_merge, x = "IncidntNum", y = "MedQ", ax = ax)
ax.set(xlabel='Homicide (montlhy count)', ylabel='Monthly Avg Weed Price ($)')
fig_4 = plot.gcf()
fig_4.savefig('fig_4.png')

# 3.2.1 OLS SF
model = sm.ols(formula = 'MedQ ~ IncidntNum', data = month_merge).fit()
model.summary()


#Second Analysis SF, restricting crimes to only those labeled as "sale of marijuana"
saleofmarijuana = sf_merged[(sf_merged['Descript'] == "SALE OF MARIJUANA")]

saleofmj_count=saleofmarijuana.groupby([saleofmarijuana.index])[['IncidntNum']].count()
# Group by date, mean(price)
price_mean=saleofmarijuana.groupby([saleofmarijuana.index])[['MedQ']].mean()
sm_df = saleofmj_count.join(price_mean)
#parse months
sm_df['month'] = pd.DatetimeIndex(sm_df.index).month
#Group by month, count IncdNUmb, mean(prices)
month_sm=sm_df.groupby(['month'])[['MedQ']].mean()
month_saleofmj=sm_df.groupby(['month'])[['IncidntNum']].count()
month_salemerge= month_sm.join(month_saleofmj)

month_salemerge.rename(columns = {"MedQ" : "Price of Medium Quality", "IncidntNum" : "Caught Selling Marijuana"}, inplace = True)

#plotting the graph
plotsellingmj = month_salemerge.plot(kind="bar",  x=month_merge.index, y="Caught Selling Marijuana")
plotsellingmj.set_ylabel("Number of People Caught Selling Marijuana")
plotsellingmj.set_xlabel("Month")



#3.2 Third Analysis SF, restricting crimes only to thoes labeles as " Drug/Narcotic" incidents
drugcrime = sf_merged[(sf_merged['Category'] == "DRUG/NARCOTIC")]

drugcrime_count=drugcrime.groupby([drugcrime.index])[['IncidntNum']].count()
# Group by date, mean(price)
pricemean=drugcrime.groupby([drugcrime.index])[['MedQ']].mean()
drug_df = drugcrime_count.join(pricemean)
# parse months
drug_df['month'] = pd.DatetimeIndex(drug_df.index).month

#Group by month, count IncdNUmb, mean(prices)
month_drug=drug_df.groupby(['month'])[['MedQ']].mean()
month_drugcr=drug_df.groupby(['month'])[['IncidntNum']].count()
month_drugmerge= month_drug.join(month_drugcr)

month_drugmerge.rename(columns = {"MedQ" : "Price of Medium Quality", "IncidntNum" : "Caught with Drug/Narcotics"}, inplace = True)

plotdrug = month_drugmerge.plot(kind="bar",  x=month_merge.index, y="Caught with Drug/Narcotics")
plotdrug.set_ylabel("Number of People Caught Selling Drugs")
plotdrug.set_xlabel("Month")
