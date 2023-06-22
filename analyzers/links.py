# links.py
import requests
import pandas as pd
from urllib.parse import urlparse
from tabulate import tabulate
from bs4 import BeautifulSoup
from scrapers.scrape import get_content_with_html, get_domain


def clean_url(url):
    parsed_url = urlparse(url)
    cleaned_query = "&".join(
        [q for q in parsed_url.query.split("&") if not q.startswith("utm_")]
    )
    return parsed_url._replace(query=cleaned_query).geturl()


def get_internal_links(url, content_html, full_report):
    
    
    soup = BeautifulSoup(content_html, "html.parser")
    rows = []

    # Get base url (including https://) from url
    base_url = url.split("//")[0] + "//" + url.split("//")[1].split("/")[0]

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and (base_url in href or href.startswith("/")):
            original_href = base_url + href if href.startswith("/") else href
            cleaned_href = clean_url(original_href)
            if full_report:  # Check if full report option is selected
                try:
                    response = requests.get(original_href, timeout=5)
                    status_code = response.status_code
                except requests.exceptions.RequestException as e:
                    status_code = "Error: " + str(e)
            else:
                status_code = (
                    "-"  # Placeholder value if full report option is not selected
                )
            rows.append([cleaned_href, link.text, status_code])
    return pd.DataFrame(
        rows, columns=["Internal Links To (Cleaned URL)", "Anchor Text", "Status Code"]
    )


