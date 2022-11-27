import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_book(books_dir, book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'

    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    path_to_save = os.path.join(books_dir, f'id{book_id}.txt')
    with open(path_to_save, 'wb') as file:
        file.write(response.content)


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

    # check_for_redirect(response)

    path_to_save = os.path.join(folder, sanitize_filename(filename) + '.txt')

    with open(path_to_save, 'wb') as file:
        file.write(response.content)

    return path_to_save


def main():
    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, 11):
        try:
            download_book(books_dir, book_id)
        except requests.HTTPError:
            print(f'Book with id {book_id} - not exist')


def parse_page_book(book_id):
    url = f'https://tululu.org/b{str(book_id)}/'

    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')

    title, author = title_tag.text.split('::')

    print(f'Заголовок: {title.strip()}')
    print(f'Автор: {author.strip()}')

    # print(image_tag['src'])
    # print()
    # print(text_block.text)


if __name__ == '__main__':
    # main()
    # parse_page_book(1)
    url = 'http://tululu.org/txt.php?id=1'

    filepath = download_txt(url, 'Алиби')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али/би', folder='books/')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али\\би', folder='txt/')
    print(filepath)  # Выведется txt/Алиби.txt
