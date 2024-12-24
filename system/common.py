# sys/common.py
import os
import sys

# Shared utilities
def log_message(message):
    if os.getenv('DEBUG', 'false').lower() == 'true':
        print(f"[LOG]: {message}")

# Filepaths
# Add the lib directory to the Python path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db.sqlite"))
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./lib"))
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/csv"))
raw_path = os.path.join(data_path, "raw")
processed_path = os.path.join(data_path, "processed")

# sys path for shared functions
sys.path.append(lib_path)

# Data analysis tasks
import json
import sqlite3 as sql3
import pandas as pd
import yfinance as yf
from datetime import datetime

# data/scraping etc 
import fitz  # PyMuPDF
import re # regex in lvr script
import csv  # Import the csv module from the standard library
import requests

try:
    from lib.metrics import calculate_metrics
    log_message("Successfully imported calculate_metrics from lib.metrics")
except ModuleNotFoundError as e:
    log_message(f"Error importing calculate_metrics: {e}")

# Log output
log_message(f"Database path: {db_path}")
log_message(f"Data directory: {data_path}")
log_message(f"Raw data directory: {raw_path}")
log_message(f"Processed data directory: {processed_path}")