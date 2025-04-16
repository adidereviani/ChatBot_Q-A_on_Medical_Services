from bs4 import BeautifulSoup

def extract_data_by_hmo_and_tier(filepath, hmo, tier):
    with open(filepath, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    tables = soup.find_all('table')
    extracted = []
    for table in tables:
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                extracted.append(f"{cols[0].text.strip()}: {cols[['מכבי','מאוחדת','כללית'].index(hmo)+1].find('strong', text=tier).parent.text.strip()}")
    return "\n".join(extracted)
