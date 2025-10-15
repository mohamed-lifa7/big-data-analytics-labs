# Big Data Analytics Module

This repository contains all the labs and coursework for my Big Data Analytics module. Each lab is organized into its own directory, containing the necessary code, notebooks, and data.

## Labs Overview

- **[Lab 1: Web Scraping](./lab1/)**: A project focused on scraping book data from the web using Python. The lab covers fetching paginated content, parsing HTML with BeautifulSoup, and storing the results in a CSV file with pandas.

- **[Lab 2: Reading Big Data Files](./lab2/)**: Explores techniques for handling datasets with large size. This lab compares the performance and memory efficiency of reading large CSV files using pandas with chunking, Dask dataframes, and various compression strategies.


## Tech Stack

- **Language**: Python 3
- **Libraries**:
    - `requests` for making HTTP requests.
    - `BeautifulSoup4` for parsing HTML.
    - `pandas` for data manipulation and storage.
    - `dask` for parallel and out-of-core computing.
    - `pyarrow` for efficient in-memory data processing.
    - `Jupyter Notebook` for interactive development.