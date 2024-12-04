from ebooklib import epub
from bs4 import BeautifulSoup

def extract_epub_content(file_path):
    book = epub.read_epub(file_path)
    chapters, titles = [], []

    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            title = soup.find(['h1', 'h2', 'h3', 'title'])
            title_text = title.get_text().strip() if title else f"Chapter {len(titles) + 1}"

            paragraphs = [p.get_text().strip() for p in soup.find_all(['p', 'div']) if p.get_text().strip()]
            if paragraphs:
                titles.append(title_text)
                chapters.append(paragraphs[1:] if len(paragraphs) > 1 else [])

    return titles, chapters
