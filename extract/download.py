from multiprocessing import Pool
import os
from urllib.error import HTTPError

from constants import (DOWNLOAD_RETRY_DELAY, DOWNLOADS_PATH,
                       MAX_DOWNLOAD_RETRY, MAX_REQUEST_RETRY, REQUEST_TIMEOUT)
from requests import Response, get
from requests.exceptions import Timeout

from extract.helpers import log
from extract.helpers.decorators import retry

FILE_NAME_TEMPLATE = '{link_title}___{link_file_name}'


@retry(MAX_REQUEST_RETRY, (HTTPError, Timeout), delay=2)
def __get_with_retry(url: str, stream=bool) -> Response:
    log.info('Iniciando requisição para ' + url)
    response = get(url, stream=stream, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    log.info('Resposta recebida de ' + url)
    return response


def __write_file(file_path: str, streamed_response):
    with open(file_path, 'wb') as local_file:
        log.info('Escrevendo arquivo ' + file_path)
        for file_chunk in streamed_response.iter_content(chunk_size=1024):
            if file_chunk:
                local_file.write(file_chunk)
    log.info(f'Arquivo {file_path} baixado.')


@retry(MAX_DOWNLOAD_RETRY, Exception, delay=DOWNLOAD_RETRY_DELAY)
def _download_file(link_title: str, link: str):
    """
    Faz o download de um arquivo do link,
    combina o `link_title` com o nome do arquivo baixado
    e salva em `DOWNLOADS_PATH`
    """
    os.makedirs(DOWNLOADS_PATH, exist_ok=True)

    response = __get_with_retry(link, stream=True)

    link_file_name = link.split('/')[-1]
    file_name = FILE_NAME_TEMPLATE.format(
        link_title=link_title,
        link_file_name=link_file_name
    )

    file_path = os.path.join(DOWNLOADS_PATH, file_name)
    __write_file(file_path, response)


def download_all(files: dict[list[str]]):
    """
    Faz o download de todos os links que devem estar em listas dentro de um dicionário para uma pasta apontada no arquivo constants.py.
    As chaves do dicionário que apontam para as listas, devem ser nomear o tipo dos arquivos daquela lista (Ex: companies, partners, mei).
    O nome de cada arquivo conterá o tipo de arquivo, o índice e o nome original do arquivo.
    """
    download_args = []

    for file_type, links in files.items():
        for i, link in enumerate(links):
            download_args.append(
                ('_'.join([file_type, str(i+1)]), link)
            )

    with Pool(len(download_args)) as p:
        list(p.starmap(_download_file, download_args))

    log.info('Todos os download foram finalizados')
