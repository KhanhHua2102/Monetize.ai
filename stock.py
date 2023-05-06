from datetime import datetime

import finnhub
import pandas as pd
import yfinance as yf
from dateutil import parser
from flask import request

import gpt
import sql
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
    response = ("Latest analyst recommendation for" + input_symbol +": Date: {}, Buy: {}, Hold: {}, Sell: {}, Strong Buy: {}, Strong Sell: {}"
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


def prompt_profit(input):
    # input = "Based on a user's input, you have to determine if they want to calculate profit. If their information does include the stock name, date added, the quantity of stock and bought price, convert those data so that it is able to input into yfinance function, must not calculate profit: {number of Shares} {Ticker} {Start-Date} {End-Date} .\nResponse must follow formats of conversion only and no need any comments or punctuation, the dates must be converted to dd/mm/yyyy, default end date is the word today no need to assume. Otherwise, please response exactly the word 'False'.\nUser message: " + input
    input = "Based on a user's message, you have to determine if the message does include a stock(share/ticker) name, a quantity of that stock, and a date; convert those input using this exact template: '{bought/sold} {number of Shares} {Ticker} {Start-Date} {End-Date}' .\nResponse must follow formats of the template only and no need any comments or punctuation, the dates must be converted to dd/mm/yyyy, default end date is the word 'today' no need to assume. If the user's message does not have enought stock's related input, please response exactly the word 'False'.\nUser message: " + input
    
    response_values = gpt.open_ai(input).split()

    print(response_values)

    check_profit = (response_values[0] != "False")

    if len(response_values) == 5:
        buy_sell = response_values[0]
        num_shares, ticker, start_date, end_date, error_msg = parse_input(response_values[1:])
        if error_msg:
            return error_msg
        
        stock_data = get_stock_data(num_shares, ticker, start_date, end_date)
        response = 'Using this information to give me a response on my stock details including start price, end price and profit if they sell it on the end date: ' + \
            stock_data[0]

        return response, check_profit, stock_data[1], buy_sell
    return None, False

def prompt_recomendation(prompt_input):
    prompt_input = "Based on a user's input, you have to determine if the users want to recommendation on a specific stock or not.If yes, should extract the message exactly in to the format:{Ticker Symbol}. Otherwise, please response exactly the word 'False'.\nUser message: " + prompt_input
    recommendation_result = gpt.openAi(prompt_input)
    print(recommendation_result + '\n')
    
    
    if "False" in recommendation_result:
        check_reccomendation = False
        result = ""
    else:
        check_reccomendation = True
        no_spaces = recommendation_result.replace(" ", "")
        analystical = analyst(no_spaces)
        result = 'Using this information to give the user an appropriate stocks recommendation: ' + analystical
 
    return result, check_reccomendation
    

# check if user message contains information about stocks, shares, and dates
# def containsStockInfo(userMessage):
#      regex = r"\b(stocks|shares|tickers)\b.*\b(\d{1,2}(st|nd|rd|th)?\s(of)?\s[A-Z][a-z]{2,8}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{2,4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}\s[A-Z][a-z]{2,8}\s\d{2,4}|\d{2,4}\s[A-Z][a-z]{2,8}\s\d{1,2}|\b(today|yesterday|tomorrow)\b)\b"
#      return bool(re.search(regex, userMessage, re.IGNORECASE))


# string="Convert this data so that it is able to input into:
# {number of Shares} {Ticker} {Start-Date} {End-Date} User message:
# I bought 200 google shares on 14/03/2022, what is my profit?
# Noted no need of comment and only pure Convertsion and make sure space in between,
# which mean you dont need to comment just the convertsion itself.
# The date  must be in dd/mm/yyyy, default endate is today date, Ticker Symbols can be input to Yfinance"
