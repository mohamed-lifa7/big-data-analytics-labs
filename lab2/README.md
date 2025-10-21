# Lab 2: Handling Large Datasets with Pandas and Dask

Directly loading large CSV files (5GB+) into memory with standard methods often leads to `MemoryError` and system crashes. This lab explores and compares strategies for efficiently reading and processing large datasets in Python.

## Project Overview

This project uses a multi-gigabyte CSV file to benchmark three primary techniques for handling big data:

1.  **Pandas Chunking**: Reading the large file in smaller, manageable pieces using the `chunksize` parameter in `pandas.read_csv()`.
2.  **Dask DataFrames**: Leveraging the `dask` library to perform out-of-core, parallel computations.
3.  **Pandas Chunking with Compression**: Analyzing the trade-offs of reading a compressed `.gzip` file directly to save disk space versus the cost of decompression time.

The methods are compared based on two key metrics: **processing time** and **storage efficiency (Peak RAM)**.

## Notebooks in this Project

This repository contains two notebooks for different environments:

1.  `colab.ipynb`: (**Easy Setup**) A full, self-contained solution designed for Google Colab. It handles everything: downloading the dataset via the Kaggle API, creating the compressed `.gz` file, and running all benchmarks.
2.  `index.ipynb`: (**Local Performance Testing**) A notebook for benchmarking on your local machine. It's ideal for comparing Pandas vs. Dask on a **multi-core CPU** (where Dask's parallelism provides a real advantage over a free-tier Colab instance). This notebook *assumes the data files already exist* in a `/data` directory.

## Dataset

The experiments are conducted on the `train.csv` file (~5.5 GB) from the [TalkingData AdTracking Fraud Detection Challenge](https://www.kaggle.com/c/talkingdata-adtracking-fraud-detection/data).

---

## How to Run

You have two options. Running in Colab is the simplest.

### Option 1: Run Everything in Google Colab (Easiest)

1.  Open the `colab.ipynb` file in Google Colab.
2.  Get your `kaggle.json` API token from your Kaggle account page.
3.  Run the setup cell and upload your `kaggle.json` when prompted.
4.  Run the rest of the cells in order. The notebook will download the data, create the compressed `.gz` file, and run all three experiments.

### Option 2: Run Locally (Best for Performance Benchmarking)

This method is best for seeing Dask's true speed on a multi-core machine, but it requires manual setup.

**Step 1: Install Local Dependencies**

You will need the Kaggle API, Pandas, Dask, and Psutil.
```sh
pip install pandas dask psutil kaggle
```
**Step 2: Download the Dataset**

1. Go to your Kaggle account page and create a new API token to download kaggle.json.

2. Place the kaggle.json file in its required directory (e.g., ~/.kaggle/kaggle.json on Linux/macOS or C:\Users\<Your-Username>\.kaggle\kaggle.json on Windows).

3. Run the Kaggle API command to download the data into a data folder:

```Bash
kaggle competitions download -c talkingdata-adtracking-fraud-detection -p ./data
```
4. Unzip the downloaded file `(talkingdata-adtracking-fraud-detection.zip)` to get `train.csv` inside the `./data` directory.

**Step 3: Create the Compressed File (Required for `index.ipynb`)**

The `index.ipynb` notebook also tests reading from a `.gz` file. You must create this file first.

You can run the following Python script (this may take several minutes):
Python

```py
import gzip
import shutil
import os

data_dir = './data'
train_file = os.path.join(data_dir, 'train.csv')
compressed_file = os.path.join(data_dir, 'train.csv.gz')

if os.path.exists(train_file):
    print(f"🗜️  Creating compressed file at {compressed_file}...")
    print("...this may take 10+ minutes, please wait...")
    
    with open(train_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print("✅ Compression complete!")
else:
    print(f"❌ Error: {train_file} not found. Please complete Step 2 first.")
```

**Step 4: Run the Local Notebook**

Once you have both `train.csv` and `train.csv.gz` in your `./data` folder, you can open and run all the cells in `index.ipynb` to see your machine's specific benchmarks.