import finnhub
import pandas as pd

# Setup client
client = finnhub.Client(api_key="ch4k2vpr01quc2n4rj5gch4k2vpr01quc2n4rj60")

# Retrieve analyst recommendations for Microsoft
recommendations = client.recommendation_trends(symbol='MSFT')
recommendations_df = pd.DataFrame(recommendations)

# Get the latest analyst recommendation
latest_recommendation = recommendations_df.iloc[0]

# Get the date of the latest recommendation
latest_date = latest_recommendation['period']

# Get the values of each element inside the recommendation
buy = latest_recommendation['buy']
hold = latest_recommendation['hold']
sell = latest_recommendation['sell']
strong_buy = latest_recommendation['strongBuy']
strong_sell = latest_recommendation['strongSell']

# Print the results
print("Latest analyst recommendation for MSFT: Date: {}, Buy: {}, Hold: {}, Sell: {}, Strong Buy: {}, Strong Sell: {}"
      .format(latest_date, buy, hold, sell, strong_buy, strong_sell))
