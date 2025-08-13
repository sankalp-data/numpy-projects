# Cryptocurrency Pump Dump Detector

## Overview
This project aims to detect potential pump-and-dump schemes in cryptocurrency markets by analyzing hourly OHLCV (Open, High, Low, Close, Volume) data.<br> The core idea is to identify unusual volume spikes that may indicate manipulation.

## Current Status
⚠️ **Work in Progress**  
The code and algorithms are still under development and not fully functional yet.<br> Features such as volume spike detection are being implemented and tested.

## Dataset

This project requires a cryptocurrency OHLCV dataset in CSV format.

You can download any sample cryptocurrency dataset (hourly or daily OHLCV) from websites like:

- [CoinGecko](https://www.coingecko.com/en/api)
- [CryptoCompare](https://min-api.cryptocompare.com/)
- [Kaggle Cryptocurrency Datasets](https://www.kaggle.com/datasets?search=cryptocurrency)

After downloading, update the file path in the code to point to the location of your CSV file. For example:

```python
data_path = r"your/relative/or/absolute/path/to/btc_hourly_ohlcv.csv"
```

## Columns Description

 - Timestamp – The specific date and time of the recorded data (hourly).
 - Open – The opening price of Bitcoin at the beginning of the hour.
 - High – The highest price reached within the hour.
 - Low – The lowest price recorded during the hour.
 - Close – The closing price of Bitcoin at the end of the hour.
 - Volume – The total trading volume within the hour.

## Note
⚡ The purpose of this project is to practice NumPy-based data analysis without using Pandas.<br>
Although Pandas could make the implementation shorter, this project intentionally sticks to NumPy for educational purposes.

## Dataset Credit
 Dataset: [Bitcoin Hourly OHLCV](https://www.kaggle.com/datasets/gauravkumar2525/bitcoin-market-hourly-trends-2024-2025?utm_medium=social&utm_campaign=kaggle-dataset-share&utm_source=twitter ) <br>
 Provided by: gauravkumar2525




