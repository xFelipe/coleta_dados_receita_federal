from extract.download import download_all
from extract.scrapping import get_url_files


def download_files():
    files = get_url_files()
    download_all(files)


if __name__ == '__main__':
    download_files()
