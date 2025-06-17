import requests

def extract_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return data

def transform_data(data):
    moeda = data['USDBRL']['code']
    valor_de_compra = data['USDBRL']['bid']
    data_timestamp = data['USDBRL']['timestamp']

    data_transformed = {
        "moeda": moeda,
        "valor_de_compra": valor_de_compra,
        "data_timestamp": data_timestamp
    }

    return data_transformed

if __name__ == "__main__":
    data = extract_data()
    transformed_data = transform_data(data)
    print(transformed_data)
