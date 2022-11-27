import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from collections import namedtuple
from urllib.parse import urljoin, urlparse, unquote


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


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


def download_image(url, filename, folder='image/'):
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


def parse_page_book(book_id):

    site = 'https://tululu.org'

    url = urljoin(site, f'b{str(book_id)}/')

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    title, author = title_tag.text.split('::')

    image_tag = soup.find('div', class_='bookimage').find('img')['src']
    image_url = urljoin(site, image_tag)

    Book = namedtuple('Book', 'title author txt_url filename image_url')
    book = Book(
        title.strip(),
        author.strip(),
        urljoin(site, f'/txt.php?id={book_id}'),
        f'{book_id}. {title.strip()}',
        image_url
    )

    return book


def main():

    for book_id in range(1, 11):
        try:
            book = parse_page_book(book_id)
            print(book.filename)
            print(book.image_url)
            filename = unquote(urlparse(book.image_url).path.split('/')[-1])
            print()
            download_image(book.image_url, filename)
            # download_txt(book.url, book.filename)
        except requests.HTTPError:
            print(f'Book with id {book_id} - not exist\n')


if __name__ == '__main__':
    main()
