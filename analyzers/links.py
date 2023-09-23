# links.py
import requests
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import urljoin
from tabulate import tabulate
from bs4 import BeautifulSoup
from scrapers.scrape import get_content_with_html, get_domain


def clean_url(url):
    parsed_url = urlparse(url)
    cleaned_query = "&".join(
        [q for q in parsed_url.query.split("&") if not q.startswith("utm_")]
    )
    return parsed_url._replace(query=cleaned_query).geturl()


def get_internal_links(url, content_html):
    soup = BeautifulSoup(content_html, "html.parser")
    base_url = urljoin(url, "/")  # Mendapatkan base URL

    internal_links = []  # Untuk menyimpan tautan internal dan teks anchor

    for link in soup.find_all("a", href=True):
        href = link.get("href")
        if href:
            absolute_url = urljoin(base_url, href)  # Membuat URL absolut
            anchor_text = link.get_text(strip=True)  # Mendapatkan teks anchor tanpa spasi

            if base_url in absolute_url:
                # Hanya menyimpan tautan yang benar-benar internal
                internal_links.append((absolute_url, anchor_text))

    return internal_links




