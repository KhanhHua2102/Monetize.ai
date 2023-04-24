from application import app,routes,models
from flask import Flask, jsonify, request, redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import config
from datetime import datetime
import openai
<<<<<<< HEAD
import os
import yfinance as yf
from dateutil import parser

=======
import yfinance as yf
from datetime import datetime
from dateutil import parser
import re
>>>>>>> origin/Long

openai.api_key = config.OPENAI_API_KEY

CORS(app)

<<<<<<< HEAD
context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path+"/../", 'test.db')

models.db.init_app(app)

def get_json_object(key,table,column_list=None):
    try:
        get_table = getattr(models,table)
        result = get_table.query.filter_by(id = key).first()
        data = {}
        if column_list is None:
            column_list = get_table.__table__.columns.keys()

        print(type(column_list))
        print(column_list)

        for column in column_list:
            try:
                get_data =  getattr(result, column)
                data[column] = get_data

            except AttributeError:
                return {'error':f"{column} is not a valid column name"}


    except AttributeError:
        return {'error': f"{table} is not a valid table name."}
    return jsonify(data)
    # return jsonify({'response',data})

# add new user to user table in database


def addUser(userId, email, password):
    get_json_object()

def addStock(userId, ticker, vol, price, date):
    pass

def updateStock(user, ticker, vol, price, date):
    pass

def addMessages():
    pass
=======
from dateutil import parser

def parse_prompt(prompt):
    try:
        num_shares, ticker, start_date_str, end_date_str = prompt.split(' ')

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

context_data = 'You are a friendly financial chatbot. The user will ask you questions, and you will provide polite responses.\n\n'
>>>>>>> origin/Long

@app.route('/generate', methods=['POST'])
def generate():
    print("prompt received")
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)

    global context_data
<<<<<<< HEAD
    context_data += 'Q: ' + prompt + '\nA: '

=======
    
    context_data += 'Q: ' + prompt + '\nA: '
    
>>>>>>> origin/Long
    def openai_completion(query):
        print("Starting GPT-3\n")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        
        response = completion.choices[0].message.content
        global context_data
        context_data += response + '\n\n'
<<<<<<< HEAD
        return response
    
    def addingstock(thisprompt):
        stock_context = "Based on a user's input, you have to determine if they want to add stocks to their portfolio. Return 'False' if they don't want to add stocks if their input is irrelevant to stocks. You should also return 'False' if their information does include the stock name, date added, the quantity of stock and bought price. Otherwise please return 'True'. For all query strictly return either True or False only and nothing else. The user input is:"
        query = stock_context+'"'+thisprompt+'"'
        response = openai_completion(query)
        if response == "True":
            return True
        return False

    def commit_database_portfolio(formatted_prompt):
        quantity,stock_type,date_added,price_bought,current_price, return_percent,return_amount,total = formatted_prompt.split(" ")
        date_added_format = datetime.strptime(date_added,'%d/%m/20%y').date()
        new_portfolio = models.portfolio1(stock_type=stock_type,date_added=date_added_format,quantity=quantity,price_bought=float(price_bought),current_price=float(current_price),return_percent=float(return_percent),return_amount=float(return_amount),total=float(total))
        models.db.session.add(new_portfolio)
        models.db.session.commit()
        models.db.session.close()


    result = openai_completion(prompt)

    return jsonify({'response': result})

with app.app_context():
    models.db.create_all()

=======
        response_values = response.split()
        if len(response_values) == 4 and response_values[0].isdigit() and all(isinstance(val, str) for val in response_values[1:]):
         num_shares, ticker, start_date, end_date, error_msg = parse_prompt(response)
         if error_msg:
        
          response = error_msg
         else:
          response = generate_response(num_shares, ticker, start_date, end_date)
          context_data = 'Using this information to give users a message:'+ response
          response = openai_completion(context_data)

        return response
    
    
    def contains_stock_info(context_data):
     # check if context_data contains information about stocks, shares, and dates
     regex = r"\b(stocks|shares|tickers)\b.*\b(\d{1,2}(st|nd|rd|th)?\s(of)?\s[A-Z][a-z]{2,8}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{2,4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}\s[A-Z][a-z]{2,8}\s\d{2,4}|\d{2,4}\s[A-Z][a-z]{2,8}\s\d{1,2}|\b(today|yesterday|tomorrow)\b)\b"
     return bool(re.search(regex, context_data, re.IGNORECASE))
      

    if contains_stock_info(prompt):
      
    # perform a specific action for when stock information is present
     print("Stock information detected in context_data. Performing specific action...")
     context_data = 'Convert this data so that it is able to input into Yfinance, must not caculate profit: {number of Shares} {Ticker} {Start-Date} {End-Date} must not caculate profit, User message: '+prompt+'Response must follow formats of convertsion only no need any comments: No need any Punctuation, the dates must be converted to dd/mm/yyyy, default end date is the word today no need to assume.' '\n'
     result = openai_completion(context_data)
    # insert your code here
    else:
     result = openai_completion(context_data)
     print("No stock information detected in context_data.")
    
    return jsonify({'response': result})

# string="Convert this data so that it is able to input into: 
# {number of Shares} {Ticker} {Start-Date} {End-Date} User message: 
# I bought 200 google shares on 14/03/2022, what is my profit? 
# Noted no need of comment and only pure Convertsion and make sure space in between, 
# which mean you dont need to comment just the convertsion itself. 
# The date  must be in dd/mm/yyyy, default endate is today date, Ticker Symbols can be input to Yfinance"
>>>>>>> origin/Long
