import requests

def extract_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    data = response.json()

    return data

print(extract_data()["USDBRL"])
