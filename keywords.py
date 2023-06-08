# File: keywords.py
from bs4 import BeautifulSoup
from pandas import DataFrame
from scrape import get_h1
import re


def check_related_keywords(content_html, related_keywords_list):
    soup = BeautifulSoup(content_html, "html.parser")
    content = soup.text.lower()
    content_length = len(content)
    related_keywords_result = []

    if content_length > 0:
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
    else:
        related_keywords_result.append(["No content available", False, "0 (0%)"])

    return DataFrame(
        related_keywords_result,
        columns=["Related Keywords", "Found in Article", "How Many Times"],
    )


def compare_seo_title_h1(seo_title, h1):
    """Compare the SEO title with the H1"""
    if seo_title == h1:
        return True
    else:
        return False


def check_primary_keyword_in_h1(primary_keyword, h1):
    pattern = re.compile(re.escape(primary_keyword), re.IGNORECASE)
    if pattern.search(h1):
        return True
    else:
        return False


def check_primary_keyword_in_headings(primary_keyword, headings):
    if primary_keyword in headings:
        return True
    else:
        return False


def check_primary_keyword_in_content(primary_keyword, content):
    # Convert both primary keyword and content to lower case to ensure case-insensitive checking
    content = content.lower()

    # Count the number of times the primary keyword appears in the content
    keyword_count = content.count(primary_keyword)

    # Compute keyword density
    keyword_density = round((keyword_count / len(content.split())) * 100, 2)

    # If the keyword count is greater than zero, the keyword is present in the content
    if keyword_count > 0:
        return [f"True, {keyword_count} times ({keyword_density}%)"]
    else:
        return [primary_keyword, "False, 0 times (0%)"]


def check_primary_in_first_p(primary_keyword, first_parapraph):
    first_parapraph = first_parapraph.lower()

    if primary_keyword in first_parapraph:
        return True
    else:
        False
