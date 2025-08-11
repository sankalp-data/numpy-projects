# Cryptocurrency Pump Dump Detector

## Overview
This project aims to detect potential pump-and-dump schemes in cryptocurrency markets by analyzing hourly OHLCV (Open, High, Low, Close, Volume) data. The core idea is to identify unusual volume spikes that may indicate manipulation.

## Current Status
⚠️ **Work in Progress**  
The code and algorithms are still under development and not fully functional yet. Features such as volume spike detection are being implemented and tested.

## Dataset

This project requires a cryptocurrency OHLCV dataset in CSV format.

You can download any sample cryptocurrency dataset (hourly or daily OHLCV) from websites like:

- [CoinGecko](https://www.coingecko.com/en/api)
- [CryptoCompare](https://min-api.cryptocompare.com/)
- [Kaggle Cryptocurrency Datasets](https://www.kaggle.com/datasets?search=cryptocurrency)

After downloading, update the file path in the code to point to the location of your CSV file. For example:

```python
data_path = r"your/relative/or/absolute/path/to/btc_hourly_ohlcv.csv"


