from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        selected_date = request.form['selected_date']
        end_date = request.form['end_date']
        shares = request.form['Shares']
        
        # get the stock data from Yahoo Finance
        stock_data = yf.download(ticker_symbol, start=selected_date, end=end_date)
        stock_name = yf.Ticker(ticker_symbol)
        # create a dictionary with the data to pass to the template
        data = {
            'ticker_symbol': ticker_symbol.upper(),
            'selected_date': selected_date,
            'end_date': end_date,
            'company_name': stock_name.info['longName'],
            'start_close_price': stock_data['Close'][0],
            'end_close_price': stock_data['Close'][-1],
            'shares': int(shares),
            'profit': float(shares) * (stock_data['Close'][-1] - stock_data['Close'][0])
        }

        return render_template('index.html', stocks=[data])

    return render_template('index.html', stocks=[])

@app.route('/get_stock_data')
def get_stock_data():
    ticker_symbol = request.args.get('ticker_symbol')
    selected_date = request.args.get('selected_date')
    end_date = request.args.get('end_date')

    # get the stock data from Yahoo Finance
    stock_data = yf.download(ticker_symbol, start=selected_date, end=end_date)
    stock_name = yf.Ticker(ticker_symbol)

    # create a dictionary with the data to return as JSON
    data = {
        'company_name': stock_name.info['longName'],
        'start_close_price': stock_data['Close'][0],
        'end_close_price': stock_data['Close'][-1]
        
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
