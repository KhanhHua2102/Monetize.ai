import openai
from flask import request

from config import Config
import sql

openai.api_key = Config.OPENAI_API_KEY


def open_ai(query, temperature=0.2):
    print("Starting GPT-3.5-turbo...\n")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.3)
    response = completion.choices[0].message.content
    return response

def open_ai_with_info(query, temperature=1):
    email = request.cookies.get('email')
    user_data = sql.get_user_data(email)[1]
    user_info = "\nUser information: \nUsername: " + user_data[0] + "\nEmail: " + user_data[1] + "\nPhone number: " + str(user_data[2])
    
    portfolio_data = sql.get_stock_data(email)[1]

    if portfolio_data == []:
        portfolio_info = "\nUser's portfolio is empty."
    else:
        portfolio_info = "\nUser's portfolio information:"
        for stock in portfolio_data:
            portfolio_info += "\nDate added: " + stock[0] + "\nTicker: " + stock[1] + "\nQuantity: " + str(stock[2]) + "\nStart price: " + str(stock[3]) + "\nEnd price: " + str(stock[4]) + "\nReturn percent: " + str(stock[5]) + "\nReturn amount: " + str(stock[6]) + "\nTotal: " + str(stock[7]) + "\n"

    query = "\n" + user_info + "\n" + portfolio_info + "\n" + query

    print(query)
    
    response = open_ai(query, temperature=temperature)
    return response