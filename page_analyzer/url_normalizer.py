from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """Нормализация входящего url (оставляет только схему и домен)"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"