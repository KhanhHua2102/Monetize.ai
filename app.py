from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
import openai
import yfinance as yf
from datetime import datetime
from dateutil import parser
import re

openai.api_key = config.OPENAI_API_KEY

CORS(app)

context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'
from dateutil import parser

def parse_prompt(prompt):
    try:
        num_shares, ticker, start_date_str, end_date_str = prompt.split(' ')

        # Parse start and end dates using dateutil parser
        start_date = parser.parse(start_date_str, fuzzy=True)
        end_date = parser.parse(end_date_str, fuzzy=True)

        # Check if start date is before end date
        if start_date >= end_date:
            raise ValueError("Invalid date range: start date must be before end date")

        # Check if end date is after today's date
        if end_date.date() > datetime.now().date():
            raise ValueError("Invalid date range: end date cannot be after today's date")

        # Convert ticker to uppercase for consistency
        ticker = ticker.upper()

        return num_shares, ticker, start_date, end_date, None
    except ValueError as e:
        # Return error message for invalid date range or prompt format
        return None, None, None, None, str(e)
    except:
        # Return error message for invalid prompt format
        return None, None, None, None, "Invalid prompt format: please enter the prompt in the format 'num_shares ticker start_date end_date'."



def generate_response(num_shares, ticker, start_date, end_date):
    try:
        # Retrieve stock info and extract company name
        stock_info = yf.Ticker(ticker).info
        company_name = stock_info['longName']

        # Retrieve historical data for specified dates
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Calculate total return
        start_price = stock_data['Close'][0]
        end_price = stock_data['Close'][-1]
        profits = (end_price - start_price) * int(num_shares)
        profit_loss = 'profit' if profits > 0 else 'loss'

        # Construct response message
        response = f"{num_shares} shares of {company_name} ({ticker}) from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}: start price = ${start_price:.2f}, end price = ${end_price:.2f}, {profit_loss} = ${profits:.2f}"
    except:
        # Return error message for invalid ticker symbol
        response = f"Invalid ticker symbol: {ticker}"

    return response


# @app.route('/generate', methods=['POST'])
# def generate():
#     print("prompt received")
#     data = request.get_json()
#     prompt = data['prompt']
#     print(prompt)

#     num_shares, ticker, start_date, end_date, error_msg = parse_prompt(prompt)

#     if error_msg:
#         # Return error message for invalid prompt format or date range
#         response = error_msg
#     else:
#         response = generate_response(num_shares, ticker, start_date, end_date)

#     return jsonify({'response': response})



def openai_completion(query):
    print("Starting GPT-3\n")
    response = ""

    if "stock price" in query:
        # Extract stock symbol from user query
        stock_symbol = query.split()[-1]
        print(f"Retrieving stock price data for {stock_symbol}")
        
        # Use yfinance to retrieve stock price data
        stock_data = yf.Ticker(stock_symbol).history(period="1d")
        latest_price = stock_data["Close"].iloc[-1]
        
        # Generate response based on stock price data
        response = f"The latest price for {stock_symbol} is {latest_price:.2f} USD."

    elif "company info" in query:
        # Extract stock symbol from user query
        stock_symbol = query.split()[-1]
        print(f"Retrieving company info for {stock_symbol}")
        
        # Use yfinance to retrieve company info data
        stock_info = yf.Ticker(stock_symbol).info
        
        # Generate response based on company info data
        response = f"Here is some information about {stock_info['longName']} ({stock_symbol}):\n\n" \
                   f"- Industry: {stock_info['industry']}\n" \
                   f"- Sector: {stock_info['sector']}\n" \
                   f"- Market Cap: {stock_info['marketCap']:.2f} USD\n" \
                   f"- Website: {stock_info['website']}"

    else:
        # Use OpenAI GPT-3 to generate a response
        completion = openai.Completion.create(
            model="text-davinci-002",
            prompt=query,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completion.choices[0].text

    print("GPT-3 response: " + response)
    return response

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    global context_data
    context_data += 'Q: ' + prompt + '\nA: '

    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        response = completion.choices[0].message.content
        global context_data
        context_data += response + '\n\n'
        return response

    result = openai_completion(context_data)
    print(context_data)
    result = openai_completion(prompt)
    return jsonify({'response': result})