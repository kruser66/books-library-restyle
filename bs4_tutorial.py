import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()
    # print(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup.prettify())

    title_tag = soup.find('main').find('header').find('h1')
    image_tag = soup.find(
        'img',
        class_='attachment-post-image size-post-image wp-post-image'
    )
    text_block = soup.find('div', class_='entry-content')
    text = text_block.get_text()

    print(title_tag.text)
    print(image_tag['src'])
    print()
    print(text)
