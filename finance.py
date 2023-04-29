import finnhub
import pandas as pd

# Setup client
client = finnhub.Client(api_key="ch4k2vpr01quc2n4rj5gch4k2vpr01quc2n4rj60")

# Retrieve analyst recommendations for Microsoft
recommendations = client.recommendation_trends(symbol='MSFT')
recommendations_df = pd.DataFrame(recommendations)

# Print the latest analyst recommendation
latest_recommendation = recommendations_df['buy'].iloc[-1]
print("Latest analyst recommendation for MSFT: ", latest_recommendation)