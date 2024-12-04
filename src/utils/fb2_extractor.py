import os
import zipfile
import xml.etree.ElementTree as ET
from app_config import AppConfig


def extract_fb2_content(file_path):
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(AppConfig.TEMP_FOLDER)
            fb2_file = [f for f in os.listdir(AppConfig.TEMP_FOLDER) if f.endswith('.fb2')][0]
            file_path = os.path.join(AppConfig.TEMP_FOLDER, fb2_file)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        raise ValueError("Unable to parse FB2 file. It may be badly formatted.")

    body = root.find(".//fb:body", AppConfig.FB2_NAMESPACE)
    if body is None:
        raise ValueError("Unable to parse FB2 file.")

    chapters = []
    titles = []

    for section in body.findall('./fb:section', AppConfig.FB2_NAMESPACE):
        title_element = section.find('./fb:title/fb:p', AppConfig.FB2_NAMESPACE)
        title_text = ' '.join(title_element.itertext()).strip() if title_element else f"Chapter {len(titles) + 1}"

        paragraphs = [' '.join(p.itertext()).strip() for p in section.findall('./fb:p', AppConfig.FB2_NAMESPACE)]
        if paragraphs:
            titles.append(title_text)
            chapters.append(paragraphs)

    return titles, chapters
