import os
import re
from bs4 import BeautifulSoup

# Directory containing HTML data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/phase2_data")

def get_all_html_text() -> str:
    """
    Loads and cleans all HTML files in the data directory.
    Extracts text, collapses multiple blank lines, and combines into a single string.
    """
    texts = []
    for fn in os.listdir(DATA_DIR):
        if not fn.endswith(".html"):
            continue
        with open(os.path.join(DATA_DIR, fn), encoding="utf-8") as f:
            raw = BeautifulSoup(f, "html.parser").get_text(separator="\n")
            cleaned = re.sub(r'\n{2,}', "\n", raw).strip()
            texts.append(cleaned)
    return "\n\n".join(texts)
