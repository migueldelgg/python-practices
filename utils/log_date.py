from datetime import datetime

def log_date():
    # formatar e retornar a hora exata para registrar logging
    today = datetime.now()

    result = today.strftime("%Y-%m-%d %X")

    return result

print(log_date())

def log_date_for_files():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def log_writer(file_name, message):

    if not file_name:
        file_name = 'log_cotacoes.txt'

    with open(f'{file_name}', 'a', encoding='utf-8') as file:
        file.write(f'{log_date()} Message: {message}\n')