import requests
from requests.exceptions import RequestException, Timeout, TooManyRedirects, SSLError
from bs4 import BeautifulSoup
import re
from domains import CONTENT_AREA
from emoji import emojize
from urllib.parse import urlparse


def get_status_code(url, max_redirects=10):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        return response.status_code

    except TooManyRedirects:
        return 302  # Too many redirects

    except SSLError:
        return 495  # SSL Certificate Error

    except Timeout:
        return 408  # Timeout error

    except RequestException:
        return 500  # Other request exceptions

    except Exception:
        return 0  # Other unknown errors

def get_domain(url):
    """Get the domain of a URL"""
    domain = url.split("//")[-1].split("/")[0].split(".")[0]
    return domain

def is_valid_url(url):
    """
    Check if the given URL is valid or not.

    Parameters:
    url (str): The URL to be checked.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    regex = re.compile(
        r"^(https?://)?"  # http:// or https:// (optional)
        r"((([A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9])|localhost)\.)+"  # domain...
        r"([A-Z]{2,6})"  # domain extension
        r"(:\d{1,5})?"  # optional port
        r"(\/.*)?$",
        re.IGNORECASE,
    )  # path (optional)
    return bool(regex.match(url))


def domain_disclaimer(url):
    """Display a disclaimer message if domain not defined in domains.py"""
    domain = get_domain(url)
    if domain not in CONTENT_AREA:
        return emojize(
            ":folded_hands:Content area is undefined, result may not be valid.",
            variant="emoji_type",
        )
    else:
        return emojize(
            ":thumbs_up: Good news! The content area has already been defined, the result should be more valid.",
            variant="emoji_type",
        )


def get_title(content_html):
    try:
        response = requests.get(content_html)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get title of webpage
        title = soup.title.string

        return title

    except:
        return "Unable to get title"


def get_html_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad status codes
    html_content = response.text
    return html_content


def get_meta_title(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        title = ""
        for tag in meta_tags:
            if (
                tag.get("property", None) == "og:title"
                or tag.get("name", None) == "title"
            ):
                title = tag.get("content", None)
                break

        if title:
            return title.strip()
        else:
            return "No meta title found"

    except Exception as e:
        return f"Unable to get meta title: {str(e)}"


def get_meta_description(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        description = ""
        for tag in meta_tags:
            if tag.get("name", None) == "description":
                description = tag.get("content", None)
                break

        if description:
            return description.strip()
        else:
            return "No meta description found"

    except Exception as e:
        return f"Unable to get meta description: {str(e)}"


def get_meta_keywords(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        keywords = []
        for tag in meta_tags:
            if tag.get("name", None) == "keywords":
                keywords_string = tag.get("content", None)
                if keywords_string:
                    keywords.extend(keywords_string.split(","))

        if keywords:
            return [keyword.strip() for keyword in keywords]
        else:
            return []

    except Exception as e:
        return f"Unable to get meta keywords: {str(e)}"


def get_canonical_url(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        canonical_url = ""
        for tag in meta_tags:
            if tag.get("rel", None) == "canonical":
                canonical_url = tag.get("href", None)
                break

        if canonical_url:
            return canonical_url.strip()
        else:
            return "No canonical URL found"

    except Exception as e:
        return f"Unable to get canonical URL: {str(e)}"


def get_author(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        author = ""
        for tag in meta_tags:
            if tag.get("name", None) == "author":
                author = tag.get("content", None)
                break

        if author:
            return author.strip()
        else:
            return "No author found"

    except Exception as e:
        return f"Unable to get author: {str(e)}"


def get_publisher(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        publisher = ""
        for tag in meta_tags:
            if tag.get("name", None) == "publisher":
                publisher = tag.get("content", None)
                break

        if publisher:
            return publisher.strip()
        else:
            return "No publisher found"

    except Exception as e:
        return f"Unable to get publisher: {str(e)}"


def get_language(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        language = ""
        for tag in meta_tags:
            if tag.get("http-equiv", None) == "Content-Language":
                language = tag.get("content", None)
                break

        if language:
            return language.strip()
        else:
            return "No language found"

    except Exception as e:
        return f"Unable to get language: {str(e)}"


def get_content(url, html_content):
    """Get the text content of a webpage without HTML elements"""
    try:
        # Parse HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")

        # Get content of webpage using class
        domain = get_domain(url)
        content_class = CONTENT_AREA.get(domain)
        if content_class:
            content = soup.find("div", class_=content_class)
        else:
            content = soup.find("body")

        # Get text from content
        if content:
            text = content.get_text()
        else:
            text = ""
        
        return text.strip()
   
    except:
        return "Unable to get content"

def get_content_with_html(url, html_content):
    """Get the content of a webpage with HTML elements"""
    try:
        # Parse HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")

        # Get content of webpage using class
        domain = get_domain(url)
        content_class = CONTENT_AREA.get(domain)
        if content_class:
            content = soup.find("div", class_=content_class)
        else:
            content = soup.find("body")
        
        return str(content)
    
    except:
        return "Unable to get content"





def get_h1(file_html):
   
    soup = BeautifulSoup(file_html, 'html.parser')
    
    # Mencari tag <h1> pertama dalam HTML
    h1_tag = soup.find('h1')
    
    # Mengembalikan teks dari tag <h1> jika ditemukan, atau None jika tidak ditemukan
    if h1_tag:
        return h1_tag.text
    else:
        return "Not Found"


  

def get_headings(content_html):
    soup = BeautifulSoup(content_html, "html.parser")
    # Mencari semua elemen heading
    headings = soup.find_all(["h1", "h2", "h3"])
    # Inisialisasi list untuk menyimpan heading
    all_headings = []
    # Perulangan untuk setiap heading
    for heading in headings:
        # Menambahkan tag sesuai dengan tipe heading
        if heading.name == "h1":
            all_headings.append(f"<H1>{heading.text}")
        elif heading.name == "h2":
            all_headings.append(f"<H2>{heading.text}")
        elif heading.name == "h3":
            all_headings.append(f"<H3>{heading.text}")

    # Mengembalikan list heading
    return all_headings


def get_first_parapraph(content):
    soup = BeautifulSoup(content, "html.parser")
    first_pargraph = soup.find("p")

    if first_pargraph:
        return first_pargraph.text.strip()
    else:
        " "
