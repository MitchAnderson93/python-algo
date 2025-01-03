# data analysis etc
import os
import sys
import json
import sqlite3 as sql3
import pandas as pd
from datetime import datetime

# data/scraping etc 
import fitz  # PyMuPDF
import re # regex in lvr script
import csv  # Import the csv module from the standard library
import requests

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import shared utilities
from system.utils.common import log_message

# Filepaths
# Add the lib directory to the Python path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db.sqlite"))
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./lib"))
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/csv"))
raw_path = os.path.join(data_path, "raw")
processed_path = os.path.join(data_path, "processed")

# Log output
log_message(f"Database path: {db_path}")
log_message(f"Data directory: {data_path}")
log_message(f"Raw data directory: {raw_path}")
log_message(f"Processed data directory: {processed_path}")