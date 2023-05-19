import openai
from flask import request

from config import Config
import sql

openai.api_key = Config.OPENAI_API_KEY


def open_ai(query, temperature=0.2):
    """Uses OpenAI's GPT-3 API to generate a response to a query

    Args:
    query (str): The query to be sent to the API
    temperature (float): The temperature of the response, which controls randomness. Higher values make the response more random and vice versa.
        (default is 0.3)

    Returns:
        response: The response from the API
    """

    print("Starting GPT-3.5-turbo...\n")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.3)
    response = completion.choices[0].message.content
    return response

def open_ai_with_info(query, temperature=1):
    """Uses OpenAI's GPT-3 API to generate a response to a query, with user information and portfolio information appended to the query

    Args:
    query (str): The query to be sent to the API
    temperature (float): The temperature of the response, which controls randomness. Higher values make the response more random and vice versa.
        (default is 1)

    Returns:
        response: The response from the API
    """

    email = request.cookies.get('email')
    user_data = sql.get_user_data(email)[1]
    user_info = "\nUser information: \nUsername: " + user_data[0] + "\nEmail: " + user_data[1] + "\nPhone number: " + str(user_data[2])

    portfolio_data = sql.get_stock_data(email)[1]
    portfolio_info = f"\nUser's risk tolerance: {user_data[3]}"
    if portfolio_data == []:
        portfolio_info += "\nUser's portfolio is empty."
    else:
        portfolio_info += "\nUser's portfolio information:"
        for stock in portfolio_data:
            portfolio_info += "\nDate added: " + stock[0] + "\nTicker: " + stock[1] + "\nQuantity: " + str(stock[2]) + "\nStart price: " + str(stock[3]) + "\nEnd price: " + str(stock[4]) + "\nReturn percent: " + str(stock[5]) + "\nReturn amount: " + str(stock[6]) + "\nTotal: " + str(stock[7]) + "\n"

    query = "\n" + user_info + "\n" + portfolio_info + "\n" + query

    print(query)
    
    try:
        response = open_ai(query, temperature=temperature)
    except:
        response = "Sorry, chatbot server is currently overloaded, please try again after a few seconds."
    return response