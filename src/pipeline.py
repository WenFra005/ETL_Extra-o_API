import requests

def extract_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    data = response.json()

    print(data)

extract_data()
