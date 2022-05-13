import os

LOCAL_DATA_PATH = '/media/felipe/BACKUP/data_science/dados_coleta_dados_receita_federal'
DOWNLOADS_PATH = os.path.join(LOCAL_DATA_PATH, 'downloads')

SCRAPPING_PAGE_LINK = 'https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj'
REQUEST_TIMEOUT = (10, 14400)  # Limite de tempo de conexão e de leitura
MAX_DOWNLOAD_RETRY = 10
DOWNLOAD_RETRY_DELAY = 120
MAX_REQUEST_RETRY = 40
