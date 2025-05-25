import json
import shutil

import requests
import pandas as pd

from utils.log_date import log_date, log_writer, log_date_for_files

log_file_name = 'log_products.txt'

def execute():
    with open(log_file_name, 'w', encoding='utf-8') as log:
        log.write(f'{log_date()} Script Inicializado\n')

    processer()

    with open(log_file_name, 'a', encoding='utf-8') as log:
        log.write(f'{log_date()} Script Finalizado\n')

def processer():
    #le o arquivo products.json e chama o format_attributes
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    format_attributes(products)

def apply_discount(price, discount):
    # metodo simples para adicionar um desconto em produto
    return price * discount

def download_image(image_uri, product_id):
    #baixa a imagem e retorna o nome do arquivo local
    file_name = f'Product_{product_id}.png'
    try:
        response = requests.get(image_uri, stream=True)
        response.raise_for_status()

        with open(file_name, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

        return file_name
    except requests.exceptions.HTTPError as http_err:
        log_writer(log_file_name, f'HTTP error occurred: {http_err}')
        return None
    except requests.exceptions.ConnectionError as conn_err:
        log_writer(log_file_name,  f'ConnectionError error occurred: {conn_err}')
        return None
    except requests.exceptions.Timeout as timeout_err:
        log_writer(log_file_name, f'Timeout error occurred: {timeout_err}')
        return None
    except requests.exceptions.RequestException as req_err:
        log_writer(log_file_name, f'Timeout error occurred: {req_err}')
        return None

def format_attributes(products):
    attributes = []

    n = 0;

    for product in products:
        n += 1

        product_id = product['id']
        title = product['title']

        description = product['description']
        short_description = f'{description[:30]}...'

        discount_price = "{:.2f}".format(apply_discount(product['price'], 0.10))

        image_local_name = download_image(product['image'], product_id)
        if not image_local_name:
            log_writer(log_file_name, f'Failed to download the image of product: {product_id}')
        else:
            log_writer(log_file_name, f'Success download image of product: {product_id}')

        attributes.append({
            'ID_Produto': product_id,
            'Titulo': title,
            'Preco_Original': product['price'],
            'Preco_Com_Desconto': discount_price,
            'Categoria': product['category'],
            'Descricao_Curta': short_description,
            'Nome_Arquivo_Imagem_Local': image_local_name
        })

        print(short_description)
        print(discount_price)
        log_writer(log_file_name, f'    Product {n}: {title} has been processed')

    products_csv(attributes)

def products_csv(products_dictionary):
    try:
        products = pd.DataFrame(products_dictionary)
        file_name = f'{log_date_for_files()} catalogo_produtos.csv'
        products.to_csv(file_name, index=False)
    except Exception as e:
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(f'{log_date()} Erro na geracao do csv: {e}\n')

execute()