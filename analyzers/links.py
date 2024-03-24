# links.py
import requests
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import urljoin
from tabulate import tabulate
from bs4 import BeautifulSoup
from scrapers.scrape import get_content_with_html, get_domain


def utm_cleaner(url):
    parsed_url = urlparse(url)
    cleaned_query = "&".join(
        [q for q in parsed_url.query.split("&") if not q.startswith("utm_")]
    )
    return parsed_url._replace(query=cleaned_query).geturl()
def link_contains_hash(url):
    # Memeriksa apakah URL mengandung karakter '#'
    return "#" in url

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

def find_duplicate_links(internal_links):
    # Buat sebuah set kosong untuk menyimpan URL tautan yang sudah ditemukan
    seen_links = set()
    
    # Buat daftar kosong untuk menyimpan tautan ganda
    duplicate_links = []
    
    for link_tuple in internal_links:
        url = link_tuple[0]  # Ambil URL dari tupel
        
        # Periksa apakah URL sudah pernah ditemukan sebelumnya
        if url in seen_links:
            duplicate_links.append(link_tuple)
        else:
            seen_links.add(url)  # Tambahkan URL ke set seen_links
    
    return duplicate_links


def count_internal_links(url, content_html):
    internal_links = get_internal_links(url, content_html)  # Memanggil fungsi get_internal_links
    return len(internal_links)

def internal_link_density(internal_links_count, article_length):
    if article_length > 0:
        internal_link_density = round((internal_links_count / article_length) * 100, 2)  # Menghitung Internal Link Density dalam persentase
        return internal_link_density
    else:
        return 0
