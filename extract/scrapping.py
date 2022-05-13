"""Reconhece os links e arquivos de download"""

from bs4 import BeautifulSoup, Tag
from constants import SCRAPPING_PAGE_LINK
from requests import get

from extract.helpers import log


def __search_companies(tag: Tag) -> bool:
    return tag.name == 'a' \
        and ('EMPRESA' in tag.text and 'Dados Abertos CNPJ' in tag.text)


def __search_partners(tag: Tag) -> bool:
    return tag.name == 'a' and 'Dados Abertos CNPJ SÓCIO' in tag.text


def get_url_files() -> dict[str, list[str]]:
    """
    Raspa títulos e links do site da receita federal.

    Retorna um dicionário com a chave sendo o tipo do arquivo,
    e o valor sendo um array de links para download
    """
    response = get(SCRAPPING_PAGE_LINK)
    soup = BeautifulSoup(response.content, 'html.parser')
    companies = soup.find_all(__search_companies)
    partners = soup.find_all(__search_partners)

    log.info(
        f'Dados raspados: {[{tag.text: tag["href"]} for tag in companies]} \
                          {[{tag.text: tag["href"]} for tag in partners]}'
    )

    return {
        'companies': [c['href'] for c in companies],
        'partners': [p['href'] for p in partners]
    }
