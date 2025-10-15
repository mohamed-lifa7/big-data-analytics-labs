# Lab 2: Handling Large Datasets with Pandas and Dask

Directly loading large CSV files (5GB+) into memory with standard methods often leads to `MemoryError` and system crashes, especially on machines with limited RAM. This lab explores and compares different strategies for efficiently reading and processing large datasets in Python.

## Project Overview

The project uses a multi-gigabyte CSV file to demonstrate and benchmark three primary techniques for handling big data:

1.  **Pandas Chunking**: Reading the large file in smaller, manageable pieces using the `chunksize` parameter in `pandas.read_csv()`.
2.  **Dask DataFrames**: Leveraging the `dask` library to perform out-of-core computations that work on datasets larger than the available RAM by using parallel processing.
3.  **Compression Techniques**: Analyzing the trade-offs of reading compressed files (`.zip`) directly to save disk space versus converting them to a more efficient columnar format like Parquet.

The methods are compared based on two key metrics: **processing time** and **storage efficiency**.

## Dataset

The experiments are conducted on the `train.csv` file (~5.5 GB) from the [TalkingData AdTracking Fraud Detection Challenge](https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data) on Kaggle.

---

## Requirements

* **Python 3.x**
* **pandas**: For chunk-based file reading.
* **dask**: For parallel, out-of-core data processing.

---

## How to Run

1.  **Clone the repository** (if you haven't already).
    ```sh
    git clone [https://github.com/mohamed-lifa7/big-data-analytics-labs.git](https://github.com/mohamed-lifa7/big-data-analytics-labs.git)
    ```

2.  **Install dependencies** from the main requirements file:
    ```sh
    pip install -r requirements.txt
    ```

3.  **Download the dataset**:
    - Go to the [Kaggle competition page](https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data).
    > you need to sumbmit to the competetion which means that you need to verify your identity.
    - Download the `train.csv.zip` file.
    - Extract it and place the `train.csv` file inside the `lab2/data/` directory.

4.  **Execute the notebook**: Run the cells in `lab2/index.ipynb` to see the performance comparison of each method.

> if you have 8Gb ram on your computer `lab2/index.ipynb` will works fine but the `lab2/compression.ipynb` file appearantlly won't work because it needs more than 8Gb, you can do it on **Google Colab** or **Kaggle** to run it without any RAM issues.

5.  **Review the findings**: The notebook contains the code and markdown cells that compare the performance and storage usage of each data handling strategy.