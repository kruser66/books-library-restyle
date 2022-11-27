import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from collections import namedtuple


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


def parse_page_book(book_id):

    site = 'https://tululu.org/'

    url = site + f'b{str(book_id)}/'

    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title, author = title_tag.text.split('::')

    Book = namedtuple('Book', 'title author url filename')
    book = Book(
        title.strip(),
        author.strip(),
        site + f'txt.php?id={book_id}',
        f'{book_id}. {title.strip()}'
    )

    return book


def main():

    for book_id in range(1, 11):
        try:
            book = parse_page_book(book_id)
            print(download_txt(book.url, book.filename))
        except requests.HTTPError:
            print(f'Book with id {book_id} - not exist')


if __name__ == '__main__':
    main()
