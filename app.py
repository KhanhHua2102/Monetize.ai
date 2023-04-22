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

def parse_prompt(prompt):
    num_shares, ticker, start_date_str, end_date_str = prompt.split(' ')

    # Convert start and end dates to datetime objects using dateutil parser
    start_date = parser.parse(start_date_str)
    end_date = parser.parse(end_date_str)

    # Convert ticker to uppercase for consistency
    ticker = ticker.upper()

    return num_shares, ticker, start_date, end_date

def generate_response(num_shares, ticker, start_date, end_date):
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

    return response

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    num_shares, ticker, start_date, end_date = parse_prompt(prompt)

    response = generate_response(num_shares, ticker, start_date, end_date)

    return jsonify({'response': response})



# @app.route('/generate', methods=['POST'])
# def generate():
#     print("prompt received")
#     data = request.get_json()
#     prompt = data['prompt']
#     print(prompt)

#     def openai_completion(query):
#         print("Starting GPT-3\n")
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
#         response = completion.choices[0].message.content
#         print("GPT-3 response: " + response)
#         return response

#     result = openai_completion(prompt)
#     return jsonify({'response': result})