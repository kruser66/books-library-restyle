import os
import requests


def download_book(books_dir, book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'

    response = requests.get(url)
    response.raise_for_status()

    path_to_save = os.path.join(books_dir, f'id{book_id}.txt')
    with open(path_to_save, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':

    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)

    for book_id in range(1, 11):
        download_book(books_dir, book_id)
