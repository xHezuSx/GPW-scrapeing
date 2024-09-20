# GPW-scrapeing
## Demo Python script scrapes financial reports from the Warsaw Stock Exchange (GPW) website based on user-defined filters.

## Features
### * **Extracts report titles, dates, types, links, and exchange rates.**
### * **Saves scraped data as a CSV file.**
### * **Downloads attachments associated with reports (if available).**

![Scraping](images/web%20scraper.jpg)

### Requirements
* Python 3.x
* Libraries:
* beautifulsoup4
* requests
* tqdm
* pandas
* os
* re

# Usage:
## Install required libraries:

###  Bash

`pip install beautifulsoup4 requests tqdm pandas os re`

## Edit the filters dictionary in the script to specify your search criteria:

* **categoryRaports** : Comma-separated list of report categories (e.g., `EBI,ESPI`).
* **typeRaports**: Comma-separated list of report types (e.g., `RB,P,Q,O,R`).
* **searchText**: Company name to search for (e.g., ASSECO).
* **date** (Optional): Date in format DD-MM-YYYY (often doesn't work on GPW site).
## Run the script:

Bash
`python script.py`

## Output
A CSV file named `scraped_data.csv` will be created in the `raporty/<company name>` directory, where `company name` is the searched company name.
If reports have downloadable attachments, they will be saved in the same directory with descriptive filenames.
The script will print information about the number of reports found and downloaded files.