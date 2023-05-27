import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_internal_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
    
    internal_links = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if href.startswith('/') or urlparse(href).netloc == '':
                internal_link = urljoin(base_url, href)
                internal_links.append(internal_link)
    
    return internal_links

def check_link_status(links):
    checked_links = []
    
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                checked_links.append((link, True))
            else:
                checked_links.append((link, False))
        except:
            checked_links.append((link, False))
    
    return checked_links

def get_link_data(url):
    internal_links = get_internal_links(url)
    link_status = check_link_status(internal_links)
    
    link_data = []
    
    for link, status in link_status:
        anchor_text = get_anchor_text(link)
        link_data.append((link, anchor_text, status))
    
    return link_data

def get_anchor_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    anchor_text = soup.get_text()
    anchor_text = anchor_text.strip() if anchor_text else ''
    
    return anchor_text
