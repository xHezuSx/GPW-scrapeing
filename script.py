from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import os
import re

# Filtry wyszukiwania dla raportów z GPW
filters = {
    'categoryRaports': 'EBI,ESPI',  # EBI - raporty dla inwestorów, ESPI - bardziej szczegółowe raporty
    'typeRaports': 'RB,P,Q,O,R',  # RB - bieżące, R - roczne, O - okresowe, Q - kwartalne, P - półroczne
    'searchText': 'asseco',  # Nazwa spółki np. ASSECO
    'date': ''  # Data w formacie 30-08-2023 (często nie działa poprawnie na stronie GPW)
}


# Funkcja do budowania URL z filtrowaniem
def build_url(filters):
    base_url = 'https://www.gpw.pl/komunikaty?categoryRaports='
    return f"{base_url}{filters['categoryRaports']}&typeRaports={filters['typeRaports']}&searchText={filters['searchText']}&date={filters['date']}"


url = build_url(filters)
print(f'Scraping: {url} ...')

# Tworzenie folderu na raporty dla danej spółki
COMPANY = filters['searchText'].upper() or 'GPW_HEAD'  # Domyślna nazwa jeśli brak spółki
os.makedirs(f'raporty/{COMPANY}', exist_ok=True)

response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

# Znalezienie głównego kontenera z wynikami raportów
report_list = soup.find('ul', attrs={'id': 'search-result', 'class': 'list'}).find_all('li')

# Listy do przechowywania danych z raportów
links = []
dates = []
timeframes = []
report_types = []
titles = []
exchange_rates = []
rate_changes = []


# Funkcja do parsowania danych z raportów
def parse_report_data(data_string):
    return data_string.split("|")[:-1]


# Funkcja do ekstrakcji liczb z tekstu (w tym formatowania na liczby zmiennoprzecinkowe)
def extract_digits(data_string):
    digits = [char for char in data_string if char.isdigit() or char == '-']
    digits.insert(-2, '.')  # Wstawienie kropki przed ostatnimi dwoma cyframi
    return float(''.join(digits))


# Pętla przetwarzająca każdy raport
for report in report_list:
    links.append('https://www.gpw.pl/' + report.find('a').get('href'))

    header = report.find('span', attrs={'class': 'date'}).getText()
    parts = [part.strip() for part in parse_report_data(header)]

    dates.append(parts[0])
    timeframes.append(parts[1])
    report_types.append(parts[2])

    titles.append(re.sub(r'\s+', ' ', report.find('a').getText().strip()))

    exchange_rate = report.find('span', attrs={'class': 'summary margin-left-30 pull-right'})
    exchange_rates.append(extract_digits(exchange_rate.text))

    rate_change = report.find('span', attrs={'class': 'loss margin-left-30 pull-right'}) or \
                  report.find('span', attrs={'class': 'profit margin-left-30 pull-right'})
    rate_changes.append(extract_digits(rate_change.text))

# Tworzenie DataFrame z zebranymi danymi
report_df = pd.DataFrame({
    'Date': dates,
    'Timeframe': timeframes,
    'Exchange Rate': exchange_rates,
    'Title': titles,
    'Rate Change': rate_changes,
    'Report Type': report_types,
    'Link': links
})

print(f'Zebrano dane z {len(links)} raportów.')
report_df.to_csv(f'raporty/{COMPANY}/scraped_data.csv', index=False)

# Pobieranie załączników
downloadable = []
attachments = []
attachment_filenames = []

for i, link in enumerate(links):
    response = requests.get(link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    report_attachments = soup.find_all('tr', attrs={'class': 'dane'})

    report_links = []
    report_filenames = []

    for attachment in report_attachments:
        file_link = 'https://espiebi.pap.pl/espi/pl/reports/view/' + attachment.find('a')['href']
        file_name = attachment.find('a').text.strip()

        report_links.append(file_link)
        report_filenames.append(file_name)

    attachment_filenames.append(report_filenames)

    if not report_attachments:
        attachments.append([f'Brak załączników PDF, raport dostępny na stronie: {link}'])
    else:
        attachments.append(report_links)
        downloadable.append(report_links)


# Funkcja do pobierania plików
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filename, 'wb') as f:
        with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                pbar.update(len(data))


# Pobieranie załączników
downloaded_files = 0
for i, attachment_group in enumerate(attachments):
    report_prefix = f'report_{i + 1}_file_'

    for j, attachment_link in enumerate(attachment_group):
        if 'Brak załączników PDF' not in attachment_link:
            file_title = re.sub(r"\s+", " ", attachment_filenames[i][j])
            print(f'Pobieranie pliku: {file_title}')
            downloaded_files += 1
            download_file(attachment_link, f'raporty/{COMPANY}/{report_prefix}{j + 1}_TITLE_{file_title}')

if downloadable:
    print(f'Pobrano {downloaded_files} plików.')
else:
    print('Brak plików do pobrania.')
