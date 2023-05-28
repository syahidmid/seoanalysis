# File: keywords.py
from bs4 import BeautifulSoup
from pandas import DataFrame

def check_related_keywords(content_html, related_keywords_list):
    soup = BeautifulSoup(content_html, 'html.parser')
    content = soup.text.lower()
    content_length = len(content)
    related_keywords_result = []
    for keyword in related_keywords_list:
        keyword = keyword.lower()
        keyword_count = content.count(keyword)
        if keyword_count > 0:
            found = True
            percentage = round((keyword_count / content_length) * 100, 2)
            how_many = f"{keyword_count} ({percentage}%)"
        else:
            found = False
            how_many = "0 (0%)"
        related_keywords_result.append([keyword, found, how_many])
    return DataFrame(related_keywords_result, columns=['Related Keywords', 'Found in Article', 'How Many Times'])

