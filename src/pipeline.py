import requests
from tinydb import TinyDB
from datetime import datetime

def extract_data():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return data

def transform_data(data):
    moeda_origem = data['USDBRL']['code']
    moeda_destino = data['USDBRL']['codein']
    valor_de_compra = data['USDBRL']['bid']
    timestamp_moeda = datetime.fromtimestamp(int(data['USDBRL']['timestamp'])).strftime('%d/%m/%Y %H:%M')
    timestamp_criacao = datetime.now().strftime('%d/%m/%Y %H:%M')

    data_transformed = {
        "moeda": moeda_origem,
        "moeda_destino": moeda_destino,
        "valor_de_compra": valor_de_compra,
        "timestamp_moeda": timestamp_moeda,
        "timestamp_criacao": timestamp_criacao

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
