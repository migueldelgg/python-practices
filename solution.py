import pandas as pd
import requests

from utils.log_date import log_date, log_writer, log_date_for_files

def execute():
    with open('log_cotacoes.txt', 'w', encoding='utf-8') as file:
            file.write(f"{log_date()} Message: Iniciando script de cotacoes. \n")

    http_service()

    log_writer('log_cotacoes.txt','Finalizado Script de Cotacoes')

def http_service():
    api_key = None
    base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        if not api_key:
            raise ValueError('Apikey nao configurada')

        log_writer('Apikey injetada')

        response = requests.get(base_url)

        if response.status_code != 200:
            raise ValueError(f'Request failed with {response.status_code} Http Status Code.')

        log_writer('log_cotacoes.txt','Request successes with 200 Http Status Code')
        data = response.json()

        try:
            conversion_rates = data['conversion_rates']

            moedas = {
                'BRL': round(conversion_rates.get('BRLS', 0), 2),
                'EUR': round(conversion_rates.get('EUR', 0), 2),
                'JPY': round(conversion_rates.get('JPY', 0), 2),
            }

            for sigla in ['BRL', 'EUR', 'JPY']:
                valor = moedas.get(sigla)
                if not valor: # Quando valor == 0.0, a condição if not valor: é verdadeira, e a linha do log é executada
                    log_writer('log_cotacoes.txt',f'{sigla} value not found.')
                log_writer('log_cotacoes.txt',f'{sigla} current value = {valor}')

        except KeyError as e:
            with open('log_cotacoes.txt', 'a', encoding='utf-8') as file:
                file.write(f'{log_date()} KeyNotFound Error: {e}\n')

        usd = 150

        result = []

        for moeda, valor_moeda in moedas.items():
            cotacao_convertida = valor_moeda * usd
            result.append({
                'Moeda_alvo': moeda,
                'Cotacao_em_Relacao_USD': f'{valor_moeda:.2f}',
                'Cotacao_convertida': f'{cotacao_convertida:.2f}'
            });

        file_name = f'{log_date_for_files()} relatorio_cotacoes.csv'

        try:
            df = pd.DataFrame(result)
            df.to_csv(file_name, index=False)
            log_writer('log_cotacoes.txt',f'CSV {file_name} Gerado com sucesso')
        except Exception as e:
            with open('log_cotacoes.txt', 'a', encoding='utf-8') as file:
                file.write(f'{log_date()} Erro na geracao do csv: {e}\n')

    except ValueError as e:
        with open('log_cotacoes.txt', 'a', encoding='utf-8') as file:
            file.write(f'{log_date()} Erro: {e}\n')

execute()