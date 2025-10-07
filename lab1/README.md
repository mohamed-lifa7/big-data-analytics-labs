# Lab 1: Python Web Scraping Case Study

This lab is a practical exercise in web scraping using Python. The goal is to extract book information from the publicly available scraping sandbox, [books.toscrape.com](http://books.toscrape.com), and save it into a structured format.

## Project Overview

The script automates the process of browsing a multi-page website to collect data. It performs three main tasks:

1.  **Fetch Content**: Programmatically navigates through all 50 pages of the website's catalogue.
2.  **Parse Data**: Extracts the **title** and **price** for every book listed.
3.  **Save Results**: Stores the collected data neatly into a CSV file.

---

## Requirements:

* **pyhton3.x**: duhh.
* **requests**: a library for loading web pages.
* **BeautifulSoup** a library for parsing HTML.
* **pandas**: duhhh

---

## How to Run

1.  **Clone the repository**
    ```sh
    git clone https://github.com/mohamed-lifa7/big-data-analytics-labs.git
    ```

2.  **Install dependencies** from the requirements file:
    ```sh
    pip install -r requirements.txt
    ```

3.  navigate into the `lab1` folder.

3.  **Execute the notebook**: Run the cells in `index.ipynb`.

4.  **Find the output**: The final scraped data will be in the `data/books.csv` file.