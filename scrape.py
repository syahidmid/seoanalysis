import requests
from bs4 import BeautifulSoup
import re
from domains import CONTENT_AREA
from emoji import emojize
from urllib.parse import urlparse

# ChatGPT d2ee59b7-b368-4a5f-b3af-2e33b7f33b4a
example_url = [
    "https://backlinko.com/actionable-seo-tips",
    "https://www.semrush.com/blog/seo-tips/",
    "https://www.wordstream.com/blog/ws/2021/03/05/seo-strategy",
    "https://ahrefs.com/blog/seo-tips/",
    "https://backlinko.com/actionable-seo-tips",
    "https://developers.google.com/search/docs/fundamentals/seo-starter-guide",
    "https://www.pcmag.com/how-to/easy-but-powerful-seo-tips-to-boost-traffic-to-your-website",
    "https://www.searchenginejournal.com/seo-tips/374673/",
    "https://www.bdc.ca/en/articles-tools/marketing-sales-export/marketing/seo-small-businesses-10-ways-rank-higher",
]


def get_status_code(url):
    response = requests.get(url)
    return response.status_code


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


def get_title(url):
    """Get the title of a webpage"""
    try:
        # Make request to webpage
        response = requests.get(url)

        # Parse webpage content using Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")

        # Get title of webpage
        title = soup.title.string

        return title

    except:
        return "Unable to get title"


def get_description(url):
    """Get the description of a webpage"""
    try:
        # Make request to webpage
        response = requests.get(url)

        # Parse webpage content using Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")

        # Get description from meta tags
        meta_tags = soup.find_all("meta")
        description = ""
        for tag in meta_tags:
            if tag.get("name", None) == "description":
                description = tag.get("content", None)

        return description

    except:
        return "Unable to get description"


def get_content(url):
    try:
        # Check if domain is registered
        parsed_url = urlparse(url)
        domain = (
            parsed_url.netloc.split(".")[-2]
            if parsed_url.netloc.count(".") >= 2
            else parsed_url.netloc
        )
        content_class = CONTENT_AREA.get(domain)

        if content_class:
            # Make request to webpage
            response = requests.get(url)

            # Parse webpage content using Beautiful Soup
            soup = BeautifulSoup(response.content, "html.parser")

            # Get content of webpage using class
            content = soup.find("div", class_=content_class)
            return content.get_text()
        else:
            # Make request to webpage
            response = requests.get(url)

            # Parse webpage content using Beautiful Soup
            soup = BeautifulSoup(response.content, "html.parser")

            # Get content of webpage using tag "body"
            content = soup.find("body")
            return content.get_text()

    except:
        return "Unable to get content"


def get_content_with_html(url):
    """Get the content of a webpage with HTML elements"""
    try:
        # Check if domain is registered
        domain = get_domain(url)
        content_class = CONTENT_AREA.get(domain)

        if content_class:
            # Make request to webpage
            response = requests.get(url)

            # Parse webpage content using Beautiful Soup
            soup = BeautifulSoup(response.content, "html.parser")

            # Get content of webpage using class
            content = soup.find("div", class_=content_class)
            return str(content)
        else:
            # Make request to webpage
            response = requests.get(url)

            # Parse webpage content using Beautiful Soup
            soup = BeautifulSoup(response.content, "html.parser")

            # Get content of webpage using tag "body"
            content = soup.find("body")
            return str(content)

    except:
        return "Unable to get content"


def get_h1(url):
    """Get the H1 of a webpage"""
    try:
        # Make request to webpage
        response = requests.get(url)

        # Parse webpage content using Beautiful Soup
        soup = BeautifulSoup(response.content, "html.parser")

        # Get H1 of webpage
        h1 = soup.find("h1").text if soup.find("h1") else None

        return h1
    except:
        return "Unable to get H1"


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
