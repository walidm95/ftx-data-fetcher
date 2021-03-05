import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter

# Import data
btc_prices = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/hourly/BTC-PERP_prices.csv")
btc_fundings = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/BTC-PERP_rates.csv")
btc_0326 = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/hourly/BTC-0326_prices.csv")
btc_0625 = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/hourly/BTC-0625_prices.csv")
btc_0924 = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/hourly/BTC-0924_prices.csv")
btc_1231 = pd.pandas.read_csv("C:/Users/walid/Desktop/Dev/ftx_data_fetcher/hourly/BTC-1231_prices.csv")

# Set time as index
btc_prices = btc_prices.set_index("startTime")
btc_fundings = btc_fundings.set_index("time")
btc_0326 = btc_0326.set_index("startTime")
btc_0625 = btc_0625.set_index("startTime")
btc_0924 = btc_0924.set_index("startTime")
btc_1231 = btc_1231.set_index("startTime")

# Keep close only
btc_prices = btc_prices[["close"]]
btc_fundings = btc_fundings[["rate"]]
btc_0326 = btc_0326[["close"]]
btc_0625 = btc_0625[["close"]]
btc_0924 = btc_0924[["close"]]
btc_1231 = btc_1231[["close"]]

# Rename columns for futures
btc_prices = btc_prices.rename(columns={"close": "price"})
btc_0326 = btc_0326.rename(columns={"close": "future"})
btc_0625 = btc_0625.rename(columns={"close": "future"})
btc_0924 = btc_0924.rename(columns={"close": "future"})
btc_1231 = btc_1231.rename(columns={"close": "future"})

# Get Premiums
startDate = "2021-01-01T00:00:00+00:00"
endDate = "2021-02-16T18:00:00+00:00"

btc_0326 = btc_0326[startDate:endDate] #temp filter
premiums_0326 = btc_prices[btc_0326.index[0]:btc_0326.index[-1]][["price"]]
premiums_0326 = premiums_0326.join(btc_0326, how="left")
premiums_0326["premium"] = (premiums_0326["future"]-premiums_0326["price"])/premiums_0326["price"]
premiums_0326 = premiums_0326.join(btc_fundings, how="left")
premiums_0326.dropna()

btc_0625 = btc_0625[startDate:endDate] #temp filter
premiums_0625 = btc_prices[btc_0625.index[0]:btc_0625.index[-1]][["price"]]
premiums_0625 = premiums_0625.join(btc_0625, how="left")
premiums_0625["premium"] = (premiums_0625["future"]-premiums_0625["price"])/premiums_0625["price"]
premiums_0625 = premiums_0625.join(btc_fundings, how="left")
premiums_0625.dropna()

btc_0924 = btc_0924[startDate:endDate] #temp filter
premiums_0924 = btc_prices[btc_0924.index[0]:btc_0924.index[-1]][["price"]]
premiums_0924 = premiums_0924.join(btc_0924, how="left")
premiums_0924["premium"] = (premiums_0924["future"]-premiums_0924["price"])/premiums_0924["price"]
premiums_0924 = premiums_0924.join(btc_fundings, how="left")
premiums_0924.dropna()

btc_1231 = btc_1231[startDate:endDate] #temp filter
premiums_1231 = btc_prices[btc_1231.index[0]:btc_1231.index[-1]][["price"]]
premiums_1231 = premiums_1231.join(btc_1231, how="left")
premiums_1231["premium"] = (premiums_1231["future"]-premiums_1231["price"])/premiums_1231["price"]
premiums_1231 = premiums_1231.join(btc_fundings, how="left")
premiums_1231.dropna()

# annualize premiums and rates
premiums_0326["days_to_expiry"] = premiums_0326.apply(lambda x: (datetime.datetime.strptime("2021-03-26T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") - datetime.datetime.strptime(x.name, "%Y-%m-%dT%H:%M:%S%z")).days, axis=1) 
premiums_0326["annualized_premium"] = premiums_0326["premium"] / premiums_0326["days_to_expiry"] * 365 * 100
premiums_0326["annualized_rate"] = premiums_0326["rate"] * 24 * 365 * 100
premiums_0326.dropna()

premiums_0625["days_to_expiry"] = premiums_0625.apply(lambda x: (datetime.datetime.strptime("2021-06-25T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") - datetime.datetime.strptime(x.name, "%Y-%m-%dT%H:%M:%S%z")).days, axis=1) 
premiums_0625["annualized_premium"] = premiums_0625["premium"] / premiums_0625["days_to_expiry"] * 365 * 100
premiums_0625["annualized_rate"] = premiums_0625["rate"] * 24 * 365 * 100
premiums_0625.dropna()

premiums_0924["days_to_expiry"] = premiums_0924.apply(lambda x: (datetime.datetime.strptime("2021-09-24T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") - datetime.datetime.strptime(x.name, "%Y-%m-%dT%H:%M:%S%z")).days, axis=1) 
premiums_0924["annualized_premium"] = premiums_0924["premium"] / premiums_0924["days_to_expiry"] * 365 * 100
premiums_0924["annualized_rate"] = premiums_0924["rate"] * 24 * 365 * 100
premiums_0924.dropna()

premiums_1231["days_to_expiry"] = premiums_1231.apply(lambda x: (datetime.datetime.strptime("2021-12-31T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z") - datetime.datetime.strptime(x.name, "%Y-%m-%dT%H:%M:%S%z")).days, axis=1) 
premiums_1231["annualized_premium"] = premiums_1231["premium"] / premiums_1231["days_to_expiry"] * 365 * 100
premiums_1231["annualized_rate"] = premiums_1231["rate"] * 24 * 365 * 100
premiums_1231.dropna()

# annualized profits
premiums_0326["annualized_profits"] = premiums_0326["annualized_rate"] - premiums_0326["annualized_premium"]
premiums_0326["annualized_profits_ma"] = premiums_0326["annualized_rate"].rolling(8).mean()

premiums_0625["annualized_profits"] = premiums_0625["annualized_rate"] - premiums_0625["annualized_premium"]
premiums_0625["annualized_profits_ma"] = premiums_0625["annualized_rate"].rolling(8).mean()

premiums_0924["annualized_profits"] = premiums_0924["annualized_rate"] - premiums_0924["annualized_premium"]
premiums_0924["annualized_profits_ma"] = premiums_0924["annualized_rate"].rolling(8).mean()

premiums_1231["annualized_profits"] = premiums_1231["annualized_rate"] - premiums_1231["annualized_premium"]
premiums_1231["annualized_profits_ma"] = premiums_1231["annualized_rate"].rolling(8).mean()

# Plot

fig, ax = plt.subplots(4,1)
btc_prices[btc_0326.index[0]:btc_0326.index[-1]].plot(ax=ax[0], y="price", title="BTC Price")
premiums_0326.plot(ax=ax[1], y="annualized_premium", title='Annualized Premium BTC-0326')
premiums_0326.plot(ax=ax[2], y="annualized_rate", title='Annualized Funding Rate BTC-0326')
premiums_0326.plot(ax=ax[3], y=["annualized_profits", "annualized_profits_ma"], title='Annualized Profits BTC-0326')
ax[3].hlines(premiums_0326["annualized_profits"].mean(), ax[3].get_xticks().min(), ax[3].get_xticks().max(), linestyle="--", color="red")
print("BTC-0326: mean of annualized profits: " + str(premiums_0326["annualized_profits"].mean()))

fig2, ax2 = plt.subplots(4,1)
btc_prices[btc_0625.index[0]:btc_0625.index[-1]].plot(ax=ax2[0], y="price", title="BTC Price")
premiums_0625.plot(ax=ax2[1], y="annualized_premium", title='Annualized Premium BTC-0625')
premiums_0625.plot(ax=ax2[2], y="annualized_rate", title='Annualized Funding Rate BTC-0625')
premiums_0625.plot(ax=ax2[3], y=["annualized_profits", "annualized_profits_ma"], title='Annualized Profits BTC-0625')
ax2[3].hlines(premiums_0625["annualized_profits"].mean(), ax2[3].get_xticks().min(), ax2[3].get_xticks().max(), linestyle="--", color="red")
print("BTC-0625: mean of annualized profits: " + str(premiums_0625["annualized_profits"].mean()))

fig3, ax3 = plt.subplots(4,1)
btc_prices[btc_0924.index[0]:btc_0924.index[-1]].plot(ax=ax3[0], y="price", title="BTC Price")
premiums_0924.plot(ax=ax3[1], y="annualized_premium", title='Annualized Premium BTC-0924')
premiums_0924.plot(ax=ax3[2], y="annualized_rate", title='Annualized Funding Rate BTC-0924')
premiums_0924.plot(ax=ax3[3], y=["annualized_profits", "annualized_profits_ma"], title='Annualized Profits BTC-0924')
ax3[3].hlines(premiums_0924["annualized_profits"].mean(), ax3[3].get_xticks().min(), ax3[3].get_xticks().max(), linestyle="--", color="red")
print("BTC-0924: mean of annualized profits: " + str(premiums_0924["annualized_profits"].mean()))

fig4, ax4 = plt.subplots(4,1)
btc_prices[btc_1231.index[0]:btc_1231.index[-1]].plot(ax=ax4[0], y="price", title="BTC Price")
premiums_1231.plot(ax=ax4[1], y="annualized_premium", title='Annualized Premium BTC-1231')
premiums_1231.plot(ax=ax4[2], y="annualized_rate", title='Annualized Funding Rate BTC-1231')
premiums_1231.plot(ax=ax4[3], y=["annualized_profits", "annualized_profits_ma"], title='Annualized Profits BTC-1231')
ax4[3].hlines(premiums_1231["annualized_profits"].mean(), ax4[3].get_xticks().min(), ax4[3].get_xticks().max(), linestyle="--", color="red")
print("BTC-1231: mean of annualized profits: " + str(premiums_1231["annualized_profits"].mean()))


# visualize futures arbitrage
"""
arb_1231_0924 = (premiums_1231["future"] - premiums_0924["future"])/premiums_0924["future"] / premiums_0924["days_to_expiry"] * 365 * 100
arb_1231_0625 = (premiums_1231["future"] - premiums_0625["future"])/premiums_0625["future"] / premiums_0625["days_to_expiry"] * 365 * 100
arb_1231_0326 = (premiums_1231["future"] - premiums_0326["future"])/premiums_0326["future"] / premiums_0326["days_to_expiry"] * 365 * 100
fig5, ax5 = plt.subplots(3,1)
arb_1231_0924[btc_1231.index[0]:btc_1231.index[-1]].plot(ax=ax5[0], title="Arb 1231-0924")
arb_1231_0625[btc_1231.index[0]:btc_1231.index[-1]].plot(ax=ax5[1], title="Arb 1231-0625")
arb_1231_0326[btc_1231.index[0]:btc_1231.index[-1]].plot(ax=ax5[2], title="Arb 1231-0326")

arb_0924_0625 = premiums_0924["annualized_premium"] - premiums_0625["annualized_premium"]
arb_0924_0326 = premiums_0924["annualized_premium"] - premiums_0326["annualized_premium"]
fig6, ax6 = plt.subplots(2,1)
arb_0924_0625[btc_0924.index[0]:btc_0924.index[-1]].plot(ax=ax6[0], title="Arb 0924-0924")
arb_0924_0326[btc_0924.index[0]:btc_0924.index[-1]].plot(ax=ax6[1], title="Arb 0924-0625")

fig7, ax7 = plt.subplots(2,1)
arb_0625_0326 = premiums_0625["annualized_premium"] - premiums_0326["annualized_premium"]
arb_0625_0326[btc_0625.index[0]:btc_0625.index[-1]].plot(ax=ax7[0], title="Arb 0625-0326")
"""
plt.show()