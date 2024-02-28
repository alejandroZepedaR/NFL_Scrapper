# Web Scraper for NFL Quarterback Stats

This Python script scrapes NFL quarterback statistics from the official NFL website and stores them in a CSV file. It utilizes BeautifulSoup for web scraping and CSV for data storage.

## Features
- Scrapes passing yards, touchdowns, interceptions, and completion percentage for NFL quarterbacks from 1970 to 2023.
- Allows querying stats by quarterback name or by year.

## Prerequisites
- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `tabulate`

## Usage
1. Clone the repository:

    ```bash
    git clone https://github.com/alejandroZepedaR/NFL_Scrapper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd /NFL_Scrapper.git
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the script:

    ```bash
    python nfl_scrapper.py
    ```

5. Follow the on-screen prompts to select options and view statistics.

## File Structure
- `nfl_scrapper.py`: Main script for scraping and interacting with the data.
- `qb.py`: Module containing classes for representing quarterbacks and their statistics.
- `all_qb_stats.csv`: CSV file to store all quarterback statistics.

## Contributors
- [Alejandro Zepeda](https://github.com/alejandroZepedaR)

