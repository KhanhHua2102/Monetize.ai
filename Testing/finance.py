from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf


CORS(app)


@app.route('/get_stock_data1111', methods=['POST'])
def get_stock_data():
    prompt = request.get_json()['prompt']
    ticker = prompt # Convert ticker to uppercase for consistency
    stock_info = yf.Ticker(ticker).info
    company_name = stock_info['longName']
    response = {'response': company_name}
    return jsonify(response)
