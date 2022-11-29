import os
import re
import sys
import requests
import argparse
from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from collections import namedtuple
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):

    if response.history:
        raise requests.HTTPError


def fetch_book_page(book_id):

    site = 'https://tululu.org/'

    url = urljoin(site, f'b{str(book_id)}/')

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    return response


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    path_to_save = os.path.join(folder, sanitize_filename(filename) + '.txt')

    with open(path_to_save, 'wb') as file:
        file.write(response.content)

    return path_to_save


def download_cover(url, filename, folder='images/'):
    """Функция для скачивания изображений книг.
    Args:
        url (str): Cсылка на картинку, которую хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранёна картинка.
    """
    os.makedirs(folder, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    path_to_save = os.path.join(folder, sanitize_filename(filename))

    with open(path_to_save, 'wb') as file:
        file.write(response.content)

    return path_to_save


def parse_book_page(response):

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    title, author = title_tag.text.split('::')

    txt_tag = soup.find(href=re.compile("/txt."))
    txt_href = txt_tag['href'] if txt_tag else '/txt.php'
    txt_url = urljoin(response.url, txt_href)

    image_tag = soup.find('div', class_='bookimage').find('img')
    image_url = urljoin(response.url, image_tag['src'])

    tag_comments = soup.find_all('div', class_='texts')
    comments = '\n'.join([tag.find('span').text for tag in tag_comments])

    tag_genre = soup.find('span', class_='d_book').find_all('a')
    genres = [tag.text for tag in tag_genre]

    Book = namedtuple(
        'Book',
        'title author txt_url image_url comments genre'
    )

    book = Book(
        title.strip(),
        author.strip(),
        txt_url,
        image_url,
        comments,
        genres
    )

    return book


def create_parser():
    parser = argparse.ArgumentParser(
        description='Парсинг книг с сайта tululu.org '
    )

    parser.add_argument(
        'start_id',
        help='Начальный индекс (int) для парсинга',
        type=int
    )
    parser.add_argument(
        'end_id',
        help='Конечный индекс (int) конечный индекс',
        type=int
    )

    return parser


def main():

    connect_wait = 10

    parser = create_parser()
    if len(sys.argv) < 3:
        parser.print_help()
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        connection = True

        while True:
            try:
                response = fetch_book_page(book_id)
                book = parse_book_page(response)

                cover_name = unquote(
                    urlparse(book.image_url).path.split('/')[-1])
                txt_name = f'{book_id}. {book.title}'

                print(download_txt(book.txt_url, txt_name))
                print(download_cover(book.image_url, cover_name))
                print()
                break
            except requests.ConnectionError:
                if connection:
                    connection = False
                    print(
                        f'\nОтсутствует соединение с Итернет!'
                        f'Повторная попытка соединения...'
                    )
                else:
                    print('\nОтсутствует соединение с Итернет!')
                    print(
                        f'Повторная попытка соединения через'
                        f' {connect_wait} секунд.'
                    )
                    sleep(connect_wait)
            except requests.HTTPError:
                print(
                    f'Книга с номером id: {book_id} ',
                    f'не доступна для скачивания.\n'
                )
                break
            except Exception as error:
                print(f'\nНепредвиденная ошибка: {error}')
                print(
                    f'\nКнига с номером id: {book_id} ',
                    f'Проверьте! Возможна ошибка при загрузке.\n'
                )


if __name__ == '__main__':
    main()
