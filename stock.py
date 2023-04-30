from datetime import datetime
from dateutil import parser
import yfinance as yf
from flask import request

import gpt
import sql


def parseInput(prompt):
    try:
        num_shares, ticker, start_date_str, end_date_str = prompt

        # Parse start and end dates using dateutil parser
        start_date = parser.parse(start_date_str, fuzzy=True)
        # Parse start date using dateutil parser
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

        return num_shares, ticker, start_date, end_date, None
    except ValueError as e:
        # Return error message for invalid date range or prompt format
        return None, None, None, None, str(e)
    except:
        # Return error message for invalid prompt format
        return None, None, None, None, "Invalid prompt format: please enter the prompt in the format 'num_shares ticker start_date end_date'."

# def addingStock(userInput):
#     stock_context = "Based on a user's input, you have to determine if they want to add stocks to their portfolio or calculate profit. Return 'False' if they don't want to add stocks or their input is irrelevant to stocks. You should also return 'True' if their information does include the stock name, date added, the quantity of stock and bought price. Otherwise please return 'True'. For all query strictly return either True or False only and nothing else. The user input is: "
#     query = stock_context+'"'+userInput+'"'
#     response = openAi(query)
#     if response == "True":
#         return True
#     return False


def getStockData(num_shares, ticker, start_date, end_date):
    try:
        # Retrieve stock info and extract company name
        stock_info = yf.Ticker(ticker).info
        company_name = stock_info['longName']

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

    return response, [start_date, ticker, num_shares, start_price, end_price, return_percent, return_amount, total]


def promptProfit(input):
    input = "Based on a user's input, you have to determine if they want to calculate profit. If their information does include the stock name, date added, the quantity of stock and bought price, convert those data so that it is able to input into yfinance function, must not calculate profit: {number of Shares} {Ticker} {Start-Date} {End-Date} .\nResponse must follow formats of conversion only and no need any comments or punctuation, the dates must be converted to dd/mm/yyyy, default end date is the word today no need to assume, and the default number of shares is 1. Otherwise, please response exactly the word 'False'.\nUser message: " + input
    response_values = gpt.openAi(input)
    response_values = response_values.split()
    if response_values == "False":
        checkProfit = False
    else:
        checkProfit = True
    if len(response_values) == 4 and response_values[0].isdigit() and all(isinstance(val, str) for val in response_values[1:]):
        num_shares, ticker, start_date, end_date, error_msg = parseInput(
            response_values)
        if error_msg:
            return error_msg
        stock_data = getStockData(num_shares, ticker, start_date, end_date)
        response = stock_data[0]
        # add stock to database
        print(getStockData(1))
        print(response + '\n')
        response = 'Using this information to give the user a response on their stock details including start price, end price and profit if they sell it on the end date: ' + response

        return response, checkProfit, stock_data[1]
    return 'format error', False


def promptReccomendation(input):
    input = "Based on a user's input, you have to determine if they contain the word recommendations in the input or not.If yes, should extract the message exactlyin to the format:{Ticker Symbol}. Otherwise, please response exactly the word 'False'.\nUser message: " + input
    response_values = gpt.openAi(input)
    response_values = response_values.split()
    if response_values == "False":
        checkProfit = False
    else:
        checkProfit = True
    return checkProfit
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
