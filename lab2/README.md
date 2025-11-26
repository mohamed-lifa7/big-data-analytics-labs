# Lab 2: Handling Large Datasets with Pandas and Dask

Directly loading large CSV files (5GB+) into memory with standard methods often leads to `MemoryError` and system crashes. This lab explores and compares strategies for efficiently reading and processing large datasets in Python.

## Project Overview

This project uses a multi-gigabyte CSV file to benchmark three primary techniques for handling big data:

1.  **Pandas Chunking**: Reading the large file in smaller, manageable pieces using the `chunksize` parameter in `pandas.read_csv()`.
2.  **Dask DataFrames**: Leveraging the `dask` library to perform out-of-core, parallel computations.
3.  **Pandas Chunking with Compression**: Analyzing the trade-offs of reading a compressed `.gzip` file directly to save disk space versus the cost of decompression time.

The methods are compared based on two key metrics: **processing time** and **storage efficiency (Peak RAM)**.

## Notebooks in this Project

This repository contains only one notebook:

1.  `kaggle.ipynb`: (**Easy Setup**) A full, self-contained solution designed for Kaggle. It handles everything: downloading the dataset via the Kaggle API, creating the compressed `.gz` file, and running all benchmarks.


## Dataset

The experiments are conducted on the `train.csv` file (7.5 GB) from the [TalkingData AdTracking Fraud Detection Challenge](https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data).

---

## How to Run

1.  Open the `kaggle.ipynb` file in kaggle.
2.  just run the notebook.