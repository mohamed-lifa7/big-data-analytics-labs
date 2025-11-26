# Lab 3: Full Data Analysis Project using Python & Power BI

## Overview

This lab demonstrates a complete data analysis workflow using Python for data preprocessing and analysis, and Power BI for visualization and reporting.
It covers all major stages of a data project — from collection and cleaning to dashboard creation and automation.

## Objectives

The main goals of this lab are to:

- Understand and implement a full data analysis pipeline.
- Clean, preprocess, and analyze real-world datasets.
- Build insightful Power BI dashboards from Python-processed data.
- Automate data workflows and updates for dynamic reporting.

## Project Components

### 1. Notebook

`index.ipynb` – The core Jupyter notebook containing:
- Data loading and cleaning.
- Exploratory Data Analysis (EDA).
- Optional predictive modeling or segmentation.
- Data export for Power BI.

### 2. Dataset

The dataset used is from the [TLC Trip Record Data - Yellow Taxi](https://www.kaggle.com/datasets/marcbrandner/tlc-trip-record-data-yellow-taxi).

You will use **Parquet files** from the **2024 Yellow Taxi data** (12 files – one per month).

Each file contains trip records with attributes such as:

- Pickup/Dropoff datetime
- Passenger count
- Trip distance
- Fares, tips, tolls, and total amount
- Pickup and dropoff locations

## Setup Instructions

1. Open `index.ipynb` in Kaggle.
2. Run all cells sequentially.
3. The notebook will:
    - Load and clean the TLC dataset.
    - Perform statistical analysis and EDA.
    - Save processed data for Power BI integration.


## Power BI Dashboard Structure
| Page                      | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| **Home Page**             | Overview of total rides, total revenue, and average fare. |
| **Trends**                | Line charts of daily and monthly performance.             |
| **Geographic Insights**   | Maps showing top pickup and dropoff zones.                |
| **Customer Segmentation** | Visual clusters based on ride patterns.                   |
| **Performance KPIs**      | Average distance, fare per mile, and trip duration.       |

## Deliverables

- Cleaned and processed dataset (map_smaple_data.csv)
- Jupyter notebook (index.ipynb)
- Power BI dashboard (.pbix file)
- README documentation (this file)

## Key Learning Outcomes

- Build an end-to-end analytical pipeline.
- Apply EDA and feature engineering techniques.
- Visualize insights interactively with Power BI.
- Automate data refresh and reporting.