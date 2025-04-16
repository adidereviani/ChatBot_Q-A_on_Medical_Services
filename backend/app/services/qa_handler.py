import os
from app.utils.html_parser import extract_data_by_hmo_and_tier

def get_context_from_html(hmo, tier):
    folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'phase2_data')
    context = ""
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            path = os.path.join(folder, filename)
            context += extract_data_by_hmo_and_tier(path, hmo, tier) + "\n"
    return context
