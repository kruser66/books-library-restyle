import os
import requests
from bs4 import BeautifulSoup


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
    parse_page_book(1)
