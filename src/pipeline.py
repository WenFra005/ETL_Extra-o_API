import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = https://www.alphavantage.co/query?from_currency=BRL&to_currency=JPY&function=CURRENCY_EXCHANGE_RATE
r = requests.get(url)
data = r.json()

print(data)