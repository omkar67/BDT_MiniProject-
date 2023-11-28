# app.py

from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import pandas as pd
import os 

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/BDT'
mongo = PyMongo(app)

# API to get the list of available stocks
@app.route('/stocks', methods=['GET'])
def get_stocks():
    unique_symbols = [
        'ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO',
        'BAJAJFINSV', 'BAJAUTOFIN', 'BAJFINANCE', 'BHARTI',
        'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA',
        'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL',
        'GRASIM', 'HCLTECH', 'HDFC', 'HDFCBANK',
        'HEROHONDA', 'HEROMOTOCO', 'HINDALC0', 'HINDALCO',
        'HINDLEVER', 'HINDUNILVR', 'ICICIBANK', 'INDUSINDBK',
        'INFOSYSTCH', 'INFRATEL', 'INFY', 'IOC',
        'ITC', 'JSWSTEEL', 'JSWSTL', 'KOTAKBANK',
        'KOTAKMAH', 'LT', 'M&M', 'MARUTI',
        'MUNDRAPORT', 'NESTLEIND', 'NTPC', 'ONGC',
        'POWERGRID', 'RELIANCE', 'SBIN', 'SESAGOA',
        'SHREECEM', 'SSLT', 'SUNPHARMA', 'TATAMOTORS',
        'TATASTEEL', 'TCS', 'TECHM', 'TELCO',
        'TISCO', 'TITAN', 'ULTRACEMCO', 'UNIPHOS',
        'UPL', 'UTIBANK', 'VEDL', 'WIPRO',
        'ZEEL', 'ZEETELE'
    ]
    return jsonify(unique_symbols)

# API to fetch stock data for the selected stock
CSV_FILE_PATH = 'stock_data.csv'

# Example of handling NaT values
@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({"error": "No stock symbol provided"})

    try:
        # Query MongoDB for stock data
        cursor = mongo.db.MainDB.find({"Symbol": symbol})
        df = pd.DataFrame(list(cursor), columns=['Date', 'Open'])

        # Drop rows with NaT values
        df = df.dropna(subset=['Date'])

        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Convert dataframe to CSV and save to file
        df.to_csv(CSV_FILE_PATH, index=False)

        # Convert dataframe to JSON
        stock_data = df.to_dict(orient='records')

        return jsonify(stock_data)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stock_data_year', methods=['GET'])
def get_stock_data_year():
    symbol = request.args.get('symbol')
    year = int(request.args.get('year'))

    if not symbol:
        return jsonify({"error": "No stock symbol provided"})

    try:
        # Query MongoDB for stock data for the specified year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        cursor = mongo.db.MainDB.find({"Symbol": symbol, "Date": {"$gte": start_date, "$lte": end_date}})
        df = pd.DataFrame(list(cursor), columns=['Date', 'Open'])

        # Drop rows with NaT values
        df = df.dropna(subset=['Date'])

        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Convert dataframe to CSV and save to file
        df.to_csv(CSV_FILE_PATH, index=False)

        # Convert dataframe to JSON
        stock_data = df.to_dict(orient='records')

        return jsonify(stock_data)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
