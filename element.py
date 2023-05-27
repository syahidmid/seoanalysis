from bs4 import BeautifulSoup
import requests

def get_all_headings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    all_headings = []

    for heading in soup.find_all(['h1', 'h2', 'h3']):
        if heading.name == 'h1':
            all_headings.append(f'<H1> {heading.text}')
        elif heading.name == 'h2':
            all_headings.append(f'<H2> {heading.text}')
        elif heading.name == 'h3':
            all_headings.append(f'<H3> {heading.text}')

    return all_headings
