from datetime import datetime

import finnhub
import pandas as pd
import requests
import yfinance as yf
from dateutil import parser

from config import Config

CLIENT = finnhub.Client(api_key=Config.FINNHUB_API_KEY)

def analyst(input_symbol):
   
    recommendations = CLIENT.recommendation_trends(symbol=input_symbol)
   
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
    response = ("Latest analyst recommendation for " + input_symbol +": Date: {}, Buy: {}, Hold: {}, Sell: {}, Strong Buy: {}, Strong Sell: {}"
      .format(latest_date, buy, hold, sell, strong_buy, strong_sell))
    return str(response)


def parse_input(prompt):
    try:
        quantity, ticker, start_date_str, end_date_str = prompt

        # Parse start and end dates using dateutil parser
        start_date = parser.parse(start_date_str, fuzzy=True)

        # Check if end date is "today" and replace with current date
        if end_date_str.lower() == "today":
            end_date = datetime.now()
        else:
            end_date = parser.parse(end_date_str, fuzzy=True)

        # Check if start date is before end date
        if start_date >= end_date:
            raise ValueError(
                "Invalid date range: start date must be before end date")

        # Check if end date is after today's date
        if end_date.date() > datetime.now().date():
            raise ValueError(
                "Invalid date range: end date cannot be after today's date")

        # Convert ticker to uppercase for consistency
        ticker = ticker.upper()

        return quantity, ticker, start_date, end_date, None
    except ValueError as e:
        # Return error message for invalid date range or prompt format
        return None, None, None, None, str(e)
    except:
        # Return error message for invalid prompt format
        return None, None, None, None, "Invalid prompt format: please enter the prompt in the format 'num_shares ticker start_date end_date'."


def get_stock_data(num_shares, ticker, start_date, end_date):
    try:
        # Retrieve stock info and extract company name
        company_name = yf.Ticker(ticker).info['longName']

        # Retrieve historical data for specified dates
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Retrieve start and end prices
        start_price = stock_data['Close'][0]
        start_price = float('{:.2f}'.format(start_price))
        end_price = stock_data['Close'][-1]
        end_price = float('{:.2f}'.format(end_price))

        # Calculate return amount
        return_amount = (end_price - start_price) * int(num_shares)
        return_amount = float('{:.2f}'.format(return_amount))
        profit_loss = 'profit' if return_amount > 0 else 'loss'

        # Calculate total return percentage
        return_percent = (end_price - start_price) / start_price * 100
        return_percent = float('{:.2f}'.format(return_percent))

        # Calculate total value of shares
        total = end_price * int(num_shares)
        total = float('{:.2f}'.format(total))

        # Construct response message
        response = f"{num_shares} shares of {company_name} ({ticker}) from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}: start price = ${start_price:.2f}, end price = ${end_price:.2f}, {profit_loss} = ${return_amount:.2f}"
    except:
        # Return error message for invalid ticker symbol
        response = f"Invalid ticker symbol: {ticker}"

    return response, (start_date, ticker, num_shares, start_price, end_price, return_percent, return_amount, total)


def prompt_profit(input_list):
    if len(input_list) == 4:
        num_shares, ticker, start_date, end_date, error_msg = parse_input(input_list)
        if error_msg:
            return error_msg
        stock_data = get_stock_data(num_shares, ticker, start_date, end_date)
        response = 'Assume that I bought or sold the stock, using this information to give me a response on my stock details including start price, end price and profit if I sell it on the end date: ' + \
            stock_data[0]

        return response, stock_data[1]
    return None, None

def prompt_recomendation(ticker):
    analystical = analyst(ticker)
    result = 'Using this information to give the me an appropriate stocks recommendation: ' + analystical

    return result


def stock_price_target(symbol):
    api_key = 'MWQ9WK5A5KFZA5U6'

    # Make a request to the Alpha Vantage API
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if 'Error Message' not in data:
        target_price = data.get('AnalystTargetPrice', 'N/A')
    
    if target_price != 'N/A':
        return target_price
    else:
        return 'No price target found for this stock'
