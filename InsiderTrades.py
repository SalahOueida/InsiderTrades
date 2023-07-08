import requests
from datetime import datetime, timedelta
import finnhub
import time


def get_insider_data():


    # Finnhub API endpoint for S&P 500 constituents
    url = 'https://finnhub.io/api/v1/index/constituents?symbol=^GSPC'
    # Replace with your Finnhub API key
    api_key = 'cijmvj1r01qgq27is74gcijmvj1r01qgq27is750'
    finnhub_client = finnhub.Client(api_key)


    # Set the request headers with the API key
    headers = {
        'X-Finnhub-Token': api_key
    }
    # Make a GET request to the API endpoint with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the stock symbols from the response
        data = response.json()
        sp500 = data['constituents']
    else:
        print('Error occurred while fetching S&P 500 constituents. API response != 200')

    # Calculate the start and end dates
    end_date = datetime.now().date()  # Current date
    start_date = end_date - timedelta(days=15)
    stock_buys = {}
    stock_sells = {}
    s = 0
    p = 0
    n = -1
    while s < 50:  # len(sp500)

        stock = sp500[s]
        buy_sum = 0
        sell_sum = 0
        try:
            insider_transactions = finnhub_client.stock_insider_transactions(
                stock, start_date, end_date)
        except:
            print('waiting... API rate limit reached')
            time.sleep(3)
            continue

        # Loading indicator
        n = -n
        p = round(s/50*100, 1)
        if p % 5 == 0:
            print(p, '%')
        elif n > 0:
            print('Loading...')

        for transaction in insider_transactions["data"]:
            
            #if transaction["symbol"] == 'WMT':
            #    print(insider_transactions["data"])

            change = transaction["change"]
            transaction_price = transaction["transactionPrice"]
            if change < 0:
                sell_sum += abs(transaction_price*change)
            else:
                buy_sum += transaction_price*change
        # print("The buy volume of",
        #      stock, "is:", format(buy_sum, ',.2f'), "$")
        # print("The sell volume of",
        #      stock, "is:", format(sell_sum, ',.2f'), "$\n")

        stock_buys[stock] = round(buy_sum, 2)
        stock_sells[stock] = round(sell_sum, 2)
        s += 1

        # print(shares)
        #price = insider_transactions[price]
        #insider_volume = insider_volume+(shares*price)

        # print(transaction)
        #shares = transaction['share']
        #price = transaction['price']
        #insider_volume = insider_volume+(shares*price)


    sorted_buys = dict(
        sorted(stock_buys.items(), key=lambda x: x[1], reverse=True))
    sorted_sells = dict(
        sorted(stock_sells.items(), key=lambda x: x[1], reverse=True))

    #print("Sorted stock_buys:")
    #for stock, buy_volume in sorted_buys.items():
    #    print(stock, ":", buy_volume)

    #print("\nSorted stock_sells:")
    #for stock, sell_volume in sorted_sells.items():
    #    print(stock, ":", sell_volume)

    return {
        'buys': sorted_buys,
        'sells': sorted_sells
    }

z = {} 
z = get_insider_data()
buys = z['buys']
sells = z['sells']

print("Sorted stock_buys:")
for stock, buy_volume in buys.items():
    print(stock, ":", format(buy_volume, ',.2f'),'$')

print("\nSorted stock_sells:")
for stock, sell_volume in sells.items():
    print(stock, ":", format(sell_volume, ',.2f'),'$')