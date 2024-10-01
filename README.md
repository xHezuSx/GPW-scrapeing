# GPW Scraping Tool

### GPW (stock exchange) Scraping Tool is a tool that allows you to download reports from the WSE stock exchange. The tool uses a scraping script that automatically downloads reports for selected companies, based on certain parameters.

![](\images\app.jpg)

## functionality

#### 1. Downloading reports for selected companies from the Stock Exchange.
#### 2. Filtering of reports based on date, report type and category.
#### 3. Ability to download attachments in PDF or HTML format.
#### 4. Exporting data to CSV file.

## Content

- `scrape_script.py`: Script responsible for downloading reports and attachments from the stock exchange.
- `user_interface.py`: Gradio-based graphical user interface for convenient parameter entry and display of results.
## Requirements

- `Python 3.12`
- Internet connection
- Windows preferred

To run the project, the following dependencies are required. All required packages can be found in the `requirements.txt` file.

On windows right click on folder where project is, select "open in terminal/CMD" option and run following command:
```bash
pip install -r requirements.txt
```

![](images\requirements.gif)
## Usage 

On windows right click on folder where project is, select "open in terminal/CMD" option and run following command: 
```bash
python .\user_interface.py
```
if everything is good you should see `Running on local URL:  http://127.0.0.1:7860`. Simply open the link and voilà :)

![](\images\run.gif)