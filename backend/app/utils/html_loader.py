import os
from bs4 import BeautifulSoup

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/phase2_data")


def get_all_html_text():
    content = ""
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".html"):
            with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                content += soup.get_text(separator="\n")
    return content
