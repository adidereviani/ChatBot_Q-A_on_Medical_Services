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



# from bs4 import BeautifulSoup
#
# def extract_data_by_hmo_and_tier(filepath, hmo, tier):
#     with open(filepath, encoding='utf-8') as f:
#         soup = BeautifulSoup(f, 'html.parser')
#
#     tables = soup.find_all('table')
#     extracted = []
#
#     for table in tables:
#         rows = table.find_all('tr')
#         if not rows:
#             continue
#
#         # Get headers (first row)
#         headers = [cell.get_text(strip=True) for cell in rows[0].find_all(['th', 'td'])]
#         if not headers or hmo not in headers:
#             continue
#
#         # Find the column index for the HMO
#         try:
#             hmo_col_idx = headers.index(hmo)
#         except ValueError:
#             continue
#
#         for row in rows[1:]:
#             cols = row.find_all('td')
#             if len(cols) <= hmo_col_idx:
#                 continue
#
#             service_name = cols[0].get_text(strip=True)
#             hmo_cell = cols[hmo_col_idx]
#
#             # Extract all tier text chunks
#             tier_text = ""
#             for line in hmo_cell.stripped_strings:
#                 if line.startswith(tier):
#                     tier_text = line
#                     break
#
#             if tier_text:
#                 extracted.append(f"{service_name} ({hmo} {tier}): {tier_text}")
#
#     return "\n".join(extracted)

