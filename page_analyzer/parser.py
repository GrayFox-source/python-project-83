import requests
from bs4 import BeautifulSoup


def parse_page(url: str) -> dict:
    """HTTP - запрос и парс основных тегов страницы"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''

    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text().strip() if h1_tag else ''

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '').strip() if meta_desc else ''

    return {
        'status_code': response.status_code,
        'title': title,
        'h1': h1,
        'description': description
    }