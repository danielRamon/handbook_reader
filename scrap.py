import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from chroma_utils import save_handbook_to_chroma


def get_chapters(base_url):
    """
    Gets all URLs from the General Handbook main page by finding links in the doc-map structure.
    Only returns chapter-level URLs without section anchors.

    Returns:
        list: List of URLs for all chapters in the handbook
    """
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract language from base_url if present
    lang_match = re.search(r'lang=([a-z]{3})', base_url)
    lang = lang_match.group(1) if lang_match else 'eng'

    # Find all links within doc-map class elements
    doc_maps = soup.find_all("ul", class_="doc-map")
    urls = []

    for doc_map in doc_maps:
        links = doc_map.find_all("a", class_="list-tile")
        for link in links:
            href = link.get('href')
            if href:
                # Remove any section anchors and query parameters
                base_href = href.split('?')[0].split('#')[0]
                # Construct full URL from relative path, including language if present
                full_url = f"https://www.churchofjesuschrist.org{base_href}?lang={lang}"
                urls.append(full_url)

    # Remove duplicates while preserving order
    unique_urls = list(dict.fromkeys(urls))

    return unique_urls


def get_sections(url):
    """
    Gets all sections from a chapter page with their titles, URLs and text content.
    Only processes sections within the body-block div.

    Args:
        url (str): URL of the chapter page

    Returns:
        dict: Dictionary with section title, URL and text content
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the body-block div first
    body_block = soup.find("div", class_="body-block")
    if not body_block:
        return {}

    sections = body_block.find_all("section")
    result = []
    for section in sections:
        # Get section title
        header = section.find("header")
        if header:
            title = header.find(re.compile(
                "h\d+")).text if header.find(re.compile("h\d+")) else ""

            # Get section URL from header link
            link = header.find("a", class_="cross-ref")
            section_id = section.get('id')
            section_url = f"https://www.churchofjesuschrist.org{link['href']}" if link else f"{url}#{section_id}"

            # Get section text
            paragraphs = section.find_all("p")
            # Exclude title number paragraph
            text = [p.text for p in paragraphs if not p.get(
                "class") or "title-number" not in p["class"]]
            text = " ".join(text)

            result.append({
                'title': title,
                'url': section_url,
                'text': text
            })

    return result


def update_handbook_data(handbook_url):
    chapters_urls = get_chapters(handbook_url)
    total_chapters = len(chapters_urls)
    handbook_data = []
    for i, chapter_url in enumerate(chapters_urls):
        chapter_sections = get_sections(chapter_url)
        if chapter_sections:
            handbook_data.append(chapter_sections)
            print(f"Progress: {int(((i+1)/total_chapters)*100)}%")
    save_handbook_to_chroma(handbook_data)


update_handbook_data(
    "https://www.churchofjesuschrist.org/study/manual/general-handbook?lang=spa")
