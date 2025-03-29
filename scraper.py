import requests
from bs4 import BeautifulSoup
import random
import time
import csv
from collections import defaultdict
from datetime import datetime

# Base URL for Environmental Sciences subject preprints
BASE_URL = "https://eartharxiv.org/repository/list/5/?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"
}

# Accepted licenses
ACCEPTED_LICENSES = [
    "CC BY",
    "CC BY-SA",
    "CC BY-NC"
]

# Store author counts to limit to 5 papers per author
author_paper_count = defaultdict(int)

# Year filter
MIN_YEAR = 2015
CURRENT_YEAR = datetime.now().year

# Output file
OUTPUT_CSV = "eartharxiv_environmental_sciences.csv"

def get_total_pages():
    """Get total number of pages in the category listing."""
    response = requests.get(BASE_URL.format(1), headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.select_one(".pagination")
    if not pagination:
        return 1
    pages = [int(a.text) for a in pagination.find_all("a") if a.text.isdigit()]
    return max(pages) if pages else 1

def get_preprint_links(page_num):
    """Return preprint URLs from a given list page."""
    url = BASE_URL.format(page_num)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select(".list-group-item h3 a")
    return ["https://eartharxiv.org" + link['href'] for link in links]

def extract_preprint_data(preprint_url):
    """Extract metadata from a single preprint page."""
    response = requests.get(preprint_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    title_tag = soup.find("h1", class_="title")
    title = title_tag.text.strip() if title_tag else "Untitled"

    # Abstract
    abstract_tag = soup.find("div", class_="abstract")
    abstract = abstract_tag.text.strip() if abstract_tag else "No abstract found."

    # Authors
    authors_div = soup.find("div", class_="authors")
    author_spans = authors_div.find_all("span") if authors_div else []
    authors = [span.get_text(strip=True) for span in author_spans]

    # DOI
    doi_tag = soup.find("a", href=lambda href: href and "doi.org" in href)
    doi = doi_tag['href'] if doi_tag else "DOI not available"

    # License
    license_tag = soup.find("a", href=lambda href: href and "creativecommons.org" in href)
    license_text = license_tag.get_text(strip=True) if license_tag else "License not available"

    # Publication date
    date_tag = soup.find("p", class_="date")
    pub_date = date_tag.text.strip() if date_tag else "Date not available"
    pub_year = extract_year(pub_date)

    return {
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "doi": doi,
        "license": license_text,
        "url": preprint_url,
        "year": pub_year,
        "date": pub_date
    }
