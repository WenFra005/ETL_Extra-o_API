import requests
from tinydb import TinyDB

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

def save_data(data, db_name="dolar_data.json"):
    db = TinyDB(db_name)
    db.insert(data)
    print("Dados salvos com sucesso no banco de dados.")
    
if __name__ == "__main__":
    data = extract_data()
    transformed_data = transform_data(data)
    save_data(transformed_data)
    print(transformed_data)
